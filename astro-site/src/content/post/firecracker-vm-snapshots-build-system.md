---
title: "Firecracker VM Snapshots: Layerfile-Performance Build Systems in Rust"
subtitle: "How webapp.io achieved 10x faster builds with VM snapshots and file dependency tracking -- and how to replicate it with Firecracker, Rust, and OverlayFS."
slug: "firecracker-vm-snapshots-build-system"
description: "Architecture and implementation plan for a Firecracker-based build system with automatic VM snapshots, file dependency tracking, and intelligent cache invalidation. The Layerfile approach rebuilt in Rust."
tags: ["firecracker", "rust", "ci-cd", "build-systems"]
author: "Dr Alexander Mikhalev"
date: "2026-05-08"
draft: false
---

webapp.io achieved 10x faster CI builds with a simple idea: instead of rebuilding from scratch each time, snapshot the VM after every successful command and only re-run steps when the files they actually read have changed.

Their Layerfile DSL looks like Dockerfile but runs commands in Firecracker VMs with automatic snapshot creation and intelligent file dependency tracking. The key innovation: only files actually *read* during build steps determine cache invalidation -- not declared dependencies.

Here is how to replicate that in Rust.

## How Layerfile Works

```
FROM vm/ubuntu:18.04

RUN apt-get update -qq
RUN apt-get install -y build-essential cmake pkg-config
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
RUN cargo install ripgrep

WORKDIR /code
COPY . .
RUN cargo build --release

RUN BACKGROUND /code/target/release/myapp
EXPOSE WEBSITE http://localhost:8000
```

Each `RUN` command executes in a Firecracker VM. After successful completion, the VM state is snapshotted. Before the next build, the system checks which files the command actually *read* (not what you declared in a `COPY`). If none of those files changed, the snapshot is restored and the step is skipped.

## The Architecture

```
Build Process:
  Parse Layerfile
    -> Check Cache Key for each instruction
    -> If cache hit (files unchanged): restore snapshot, skip
    -> If cache miss: execute in VM, track file reads, create snapshot

Cache Decision:
  For each instruction:
    1. Compute cache key (instruction hash + dependency file hashes + previous state)
    2. Compare dependency files against current state
    3. If all match: restore snapshot, skip execution
    4. If any differ: re-execute, re-snapshot
```

## The Three Core Components

### 1. Layerfile Parser

Parse the DSL into typed instructions:

```rust
#[derive(Debug, Clone)]
pub enum Instruction {
    From { image: String },
    Run { command: String },
    Copy { src: String, dest: String },
    Env { key: String, value: String },
    Workdir { path: String },
    Background { command: String },
    ExposeWebsite { url: String },
}

pub fn parse_layerfile(input: &str) -> Result<Vec<Instruction>> {
    let mut instructions = Vec::new();
    for line in input.lines() {
        let line = line.trim();
        if line.is_empty() || line.starts_with('#') {
            continue;
        }
        let (keyword, rest) = line.split_once(' ')
            .ok_or_else(|| anyhow!("Invalid line: {}", line))?;
        let instruction = match keyword.to_uppercase().as_str() {
            "FROM" => Instruction::From { image: rest.to_string() },
            "RUN" => Instruction::Run { command: rest.to_string() },
            "COPY" => {
                let (src, dest) = rest.split_once(' ')
                    .ok_or_else(|| anyhow!("COPY needs src and dest"))?;
                Instruction::Copy { src: src.to_string(), dest: dest.to_string() }
            }
            "ENV" => {
                let (key, value) = rest.split_once(' ')
                    .ok_or_else(|| anyhow!("ENV needs key and value"))?;
                Instruction::Env { key: key.to_string(), value: value.to_string() }
            }
            "WORKDIR" => Instruction::Workdir { path: rest.to_string() },
            "BACKGROUND" => Instruction::Background { command: rest.to_string() },
            "EXPOSE" => Instruction::ExposeWebsite { url: rest.to_string() },
            _ => bail!("Unknown instruction: {}", keyword),
        };
        instructions.push(instruction);
    }
    Ok(instructions)
}
```

### 2. File Dependency Tracking

This is the secret sauce. Three options, in order of complexity:

**Option A: OverlayFS (Simplest)**

Mount the build directory as an overlay. After each command, inspect the upper layer to see which files were copied/modified. This catches writes but not reads.

```rust
pub struct OverlayTracker {
    lower: PathBuf,
    upper: PathBuf,
    work: PathBuf,
}

impl OverlayTracker {
    pub fn mount(&self) -> Result<()> {
        let opts = format!(
            "lowerdir={},upperdir={},workdir={}",
            self.lower.display(),
            self.upper.display(),
            self.work.display()
        );
        mount(Some("overlay"), "/mnt/build", Some("overlay"),
              MsFlags::empty(), Some(&opts))?;
        Ok(())
    }

    pub fn get_accessed_files(&self) -> Result<HashSet<PathBuf>> {
        let mut accessed = HashSet::new();
        for entry in WalkDir::new(&self.upper) {
            accessed.insert(entry?.path().to_owned());
        }
        Ok(accessed)
    }
}
```

**Option B: ptrace**

Attach to the child process via ptrace and intercept `open`/`openat` syscalls. Records every file the process reads. Higher overhead but captures reads accurately.

**Option C: eBPF**

Attach eBPF programs to `do_sys_open` and trace file access with near-zero overhead. Requires root but gives kernel-level accuracy.

### 3. Snapshot Management

```rust
pub struct SnapshotManager {
    cache_dir: PathBuf,
}

impl SnapshotManager {
    pub async fn create_snapshot(&self, vm: &FirecrackerVM, key: &str) -> Result<()> {
        let snapshot_path = self.cache_dir.join(format!("{}.snap", key));
        vm.create_snapshot(&snapshot_path).await?;
        Ok(())
    }

    pub async fn restore_snapshot(&self, vm: &mut FirecrackerVM, key: &str) -> Result<()> {
        let snapshot_path = self.cache_dir.join(format!("{}.snap", key));
        if snapshot_path.exists() {
            vm.restore_snapshot(&snapshot_path).await?;
            Ok(())
        } else {
            bail!("Snapshot not found: {}", key)
        }
    }

    pub fn compute_cache_key(
        &self,
        instruction: &Instruction,
        dependencies: &HashSet<PathBuf>,
    ) -> String {
        let mut hasher = Sha256::new();
        hasher.update(format!("{:?}", instruction).as_bytes());
        for dep in dependencies {
            if let Ok(contents) = fs::read(dep) {
                hasher.update(&contents);
            }
        }
        format!("{:x}", hasher.finalize())
    }
}
```

## The Executor

Tying it all together:

```rust
pub struct LayerfileExecutor {
    vm_manager: VMManager,
    tracker: OverlayTracker,
    cache: SnapshotManager,
    dependencies: HashMap<usize, HashSet<PathBuf>>,
}

impl LayerfileExecutor {
    pub async fn execute(&mut self, layerfile: &str) -> Result<()> {
        let instructions = parse_layerfile(layerfile)?;

        for (idx, instruction) in instructions.iter().enumerate() {
            // Check if we can skip this step
            if let Some(deps) = self.dependencies.get(&idx) {
                let cache_key = self.cache.compute_cache_key(instruction, deps);
                if self.cache.has_snapshot(&cache_key).await? {
                    if !self.any_file_changed(deps)? {
                        println!("Cache hit for step {}", idx);
                        let mut vm = self.vm_manager.create_vm().await?;
                        self.cache.restore_snapshot(&mut vm, &cache_key).await?;
                        continue;
                    }
                }
            }

            // Execute and track
            let mut vm = self.vm_manager.create_vm().await?;
            self.tracker.mount()?;
            vm.execute(instruction).await?;
            let file_deps = self.tracker.get_accessed_files()?;

            // Snapshot after successful execution
            let cache_key = self.cache.compute_cache_key(instruction, &file_deps);
            self.cache.create_snapshot(&vm, &cache_key).await?;
            self.dependencies.insert(idx, file_deps);
        }

        Ok(())
    }
}
```

## Performance Characteristics

| Scenario | Traditional Docker | Snapshot System | Speedup |
|----------|-------------------|-----------------|---------|
| No changes | Rebuild everything | Skip all (<1s) | 100x+ |
| Code change only | Rebuild from COPY | Skip dependencies | 10x |
| Config change | Full rebuild | Partial rebuild | 5x |
| First build | Normal | Normal + snapshot overhead | 0.9x |

Cold start: VM boot ~125ms + execution + snapshot ~1s.
Warm start (cache hit): Cache check ~5ms + snapshot restore ~8ms.

## Connection to Terraphim Infrastructure

This system is the foundation for the [Terraphim GitHub Runner](/post/terraphim-github-runner-firecracker/). Instead of booting a fresh VM for every CI job, the runner restores snapshots from previous builds. Combined with [Learning via Negativa](/post/learning-via-negativa-ai-memory/) for tracking which workflows share dependencies, the system learns which snapshots to keep warm.

The minimal implementation requires approximately 1,500 lines of Rust code. The four-week roadmap:

1. **Week 1**: Layerfile parser + basic Firecracker VM control
2. **Week 2**: File tracking with OverlayFS + dependency storage
3. **Week 3**: Snapshot management + cache logic
4. **Week 4**: Integration testing + performance tuning

## Key Insights

File tracking is the secret sauce -- monitor actual file reads, not declared dependencies. Snapshots are automatic -- after every successful instruction. Cache invalidation is precise -- only rebuild when tracked files change. VM overhead is amortised -- reuse across multiple builds.

The result: 10x faster builds with VM-level isolation and no dependency declaration required.

---

*Terraphim AI uses Firecracker VMs throughout its infrastructure for AI agent isolation, CI/CD, and build systems. [Learn more](https://terraphim.ai).*
