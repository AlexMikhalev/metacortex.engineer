---
title: "Terraphim GitHub Runner: AI-Powered CI/CD with Firecracker MicroVMs"
subtitle: "Sub-2-second VM boot times. LLM-based workflow parsing. Kernel-level isolation per build. A CI/CD system built for privacy-sensitive Rust projects."
slug: "terraphim-github-runner-firecracker"
description: "How Terraphim GitHub Runner combines LLM-powered workflow understanding with Firecracker microVM isolation for secure, private, and fast GitHub Actions execution."
tags: ["ci-cd", "firecracker", "rust", "devops"]
author: "Dr Alexander Mikhalev"
date: "2026-05-11"
draft: false
---

Traditional CI/CD runners face three fundamental challenges: shared runners expose your code to other users, cold VMs take minutes to boot, and static parsers cannot understand complex workflows.

Terraphim GitHub Runner solves all three with isolated Firecracker microVM execution, sub-2-second boot times, and AI-powered workflow parsing.

## AI-Powered Workflow Parsing

The system uses an LLM-based workflow parser that understands intent, not just YAML structure:

```yaml
# Your GitHub Actions workflow
name: Test CI
on: [pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Run tests
        run: cargo test --verbose
```

Gets transformed by the LLM into:

```json
{
  "name": "Test CI",
  "steps": [
    {
      "name": "Run tests",
      "command": "cargo test --verbose",
      "working_dir": "/workspace",
      "timeout_seconds": 300
    }
  ],
  "setup_commands": ["git clone $REPO_URL /workspace"],
  "cache_paths": ["target/"]
}
```

The LLM understands:

- **Action translation**: Converts GitHub Actions to shell commands
- **Dependency detection**: Identifies step dependencies automatically
- **Environment extraction**: Finds required environment variables
- **Smart caching**: Suggests cache paths for optimisation

## Firecracker MicroVM Isolation

Every workflow runs in its own Firecracker microVM with:

### Security

- **Kernel isolation**: Separate Linux kernel per VM
- **No network access** by default (configurable)
- **Resource limits**: CPU and memory constraints enforced
- **Snapshot/rollback**: Instant recovery from failures

### Performance

- **Sub-2-second boot**: VMs start in approximately 1.5 seconds
- **Sub-500ms allocation**: New sessions in approximately 300ms
- **Minimal overhead**: MicroVM kernels, not full OS

## Architecture

```
GitHub Repository
    |
    v
Terraphim GitHub Runner Server
    |-- HMAC-SHA256 Signature Verification
    |-- Workflow Discovery (.github/workflows/*.yml)
    |-- LLM Workflow Parser (Ollama/OpenRouter)
    |-- Firecracker VM Provider
        |-- SessionManager (VM lifecycle)
        |-- VmCommandExecutor (HTTP API)
        |-- LearningCoordinator (pattern tracking)
    |
    v
Firecracker API (fcctl-web)
    |-- fc-vm-1 (UUID: abc)
    |-- fc-vm-2 (UUID: def)
    |-- fc-vm-3 (UUID: ghi)
```

## Performance Benchmarks

| Metric | Value | Notes |
|--------|-------|-------|
| **VM Boot Time** | ~1.5s | Firecracker microVM with Ubuntu |
| **VM Allocation** | ~300ms | Including ID generation |
| **Workflow Parsing (LLM)** | ~500-2000ms | Depends on workflow complexity |
| **Workflow Parsing (Simple)** | ~1ms | YAML-only parsing |
| **End-to-End Latency** | ~2.5-4s | Webhook to VM execution |

Throughput: 10+ workflows per second per server instance.

## Privacy-First Design

- **Local LLM**: Use Ollama for on-premises AI (no data leaves your infrastructure)
- **Cloud option**: OpenRouter for teams that prefer cloud LLMs
- **No telemetry**: Zero data sent to external services

## Getting Started

```bash
# Clone repository
git clone https://github.com/terraphim/terraphim-ai.git
cd terraphim-ai

# Build with Ollama support
cargo build --release -p terraphim_github_runner_server --features ollama

# Install Ollama (if using LLM features)
curl -fsSL https://ollama.com/install.sh | sh
ollama pull gemma3:4b

# Start server
USE_LLM_PARSER=true \
OLLAMA_BASE_URL=http://127.0.0.1:11434 \
OLLAMA_MODEL=gemma3:4b \
GITHUB_WEBHOOK_SECRET=your_secret \
FIRECRACKER_API_URL=http://127.0.0.1:8080 \
./target/release/terraphim_github_runner_server
```

## Pattern Learning

The system tracks execution patterns to optimise future runs:

- Success rate by command type
- Average execution time
- Common failure patterns
- Optimal cache paths
- Timeout recommendations

## Use Cases

### Privacy-Sensitive Projects

Financial, healthcare, and government code where shared runners are not acceptable. Each build runs in its own isolated kernel.

### Rust Project CI

```yaml
name: Rust CI
on: [pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build
        run: cargo build --release
      - name: Test
        run: cargo test --verbose
```

Terraphim executes this in an isolated Firecracker VM with automatic workspace mounting, Rust dependency caching, and parallel test execution.

### Multi-Language Projects

Parallel VM allocation for frontend, backend, and integration jobs. Language-specific environment setup. Docker-in-Firecracker support.

## Connection to the AI Dark Factory

The GitHub Runner is a component of the broader [AI Dark Factory](/post/deploying-ai-dark-factory/) architecture. ADF agents use Firecracker VMs for isolated execution, and the GitHub Runner extends this to CI/CD workloads. Combined with [Sentrux quality gates](/post/sentrux-quality-gates-ai-code/), the full pipeline becomes: AI agent writes code, GitHub Runner builds it in an isolated VM, Sentrux checks architectural quality, PR merges or fails.

---

*Terraphim GitHub Runner is part of the Terraphim AI workspace. [Learn more](https://github.com/terraphim/terraphim-ai).*
