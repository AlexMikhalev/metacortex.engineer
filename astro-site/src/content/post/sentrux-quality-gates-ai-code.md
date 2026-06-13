---
title: "Sentrux Quality Gates: Closing the Feedback Loop on AI-Generated Code"
subtitle: "Traditional CI catches syntax errors and test failures. Sentrux catches architectural degradation -- before a single AI agent can turn a clean codebase into spaghetti."
slug: "sentrux-quality-gates-ai-code"
description: "How Sentrux structural quality sensors integrate with the AI Dark Factory to measure modularity, acyclicity, and complexity before and after AI-generated code changes."
tags: ["ci-cd", "code-quality", "ai-agents", "architecture"]
author: "Dr Alexander Mikhalev"
date: "2026-05-13"
draft: false
---

AI agents write code faster than humans can review it. A single session might touch 50 files, introduce new dependencies, and refactor core modules -- all in minutes. Without structural governance, codebases decay at machine speed.

Today we are announcing Sentrux quality gates, now integrated across all Terraphim projects.

## The Problem: Code Quality at Machine Speed

The failure modes are predictable:

- **Tangled dependencies** -- Modules that started clean become spaghetti
- **God files** -- Single files accumulate 36+ dependencies
- **Complexity creep** -- Functions grow to 254+ cyclomatic complexity
- **Silent degradation** -- Quality drops 500 points before anyone notices

Traditional CI catches syntax errors and test failures, but it does not catch *architectural* degradation. That is where Sentrux comes in.

## Meet Sentrux

[Sentrux](https://github.com/sentrux/sentrux) is a Rust-based structural quality sensor that watches your codebase in real-time. It computes a **quality signal** (0-10000) from 5 root cause metrics:

| Metric | What It Catches |
|--------|----------------|
| **Modularity** | God files, tight coupling, hotspots |
| **Acyclicity** | Circular dependencies |
| **Depth** | Deep dependency chains |
| **Equality** | Complexity concentration (Gini coefficient) |
| **Redundancy** | Dead code, duplicates |

Unlike linters that check style, Sentrux checks *structure*. It answers: "Does this change fit the system? Will this abstraction cause problems as the codebase grows?"

## Integration at Three Levels

### 1. CI Quality Gates

Every PR runs a quality check:

```yaml
# .github/workflows/sentrux-quality-gate.yml
- name: Run Sentrux Check
  run: sentrux check .

- name: Check Delta
  run: |
    if [ $DELTA -lt -100 ]; then
      echo "Quality degraded! Blocking merge."
      exit 1
    fi
```

Automatic baseline comparison. PR comments with quality reports. Merge blocking on degradation. Per-project rules via `.sentrux/rules.toml`.

### 2. Agent Integration

The ADF build-runner now measures quality before and after builds:

```bash
# Before: quality = 7342
sentrux check .

# Build and test
cargo test

# After: quality = 6891 (degraded!)
sentrux check .
```

Build status now includes the quality signal: `fmt+clippy+test pass | quality: 5241`

### 3. MCP Server

Agents query Sentrux directly via MCP:

```
Agent: scan("/path/to/project")
  -> { quality_signal: 7342, bottleneck: "modularity" }

Agent: session_start()
  -> { status: "Baseline saved" }

... writes code ...

Agent: session_end()
  -> { pass: false,
      signal_before: 7342,
      signal_after: 6891,
      summary: "Quality degraded" }
```

## Real Results

After scanning our own projects:

| Project | Quality | Key Finding |
|---------|---------|-------------|
| **gitea-robot** | **8648** | Clean Go codebase, minimal issues |
| **terraphim-ai** | **5241** | 1 god file (orchestrator/src/lib.rs, fan-out=36) |
| **gitea** | **3847** | Large upstream fork with accumulated debt |
| **atomic-server** | **3271** | Needs attention |

The terraphim-ai god file is already on our refactoring roadmap. Without Sentrux, we might not have quantified the impact so clearly.

This connects directly to the [AI Dark Factory deployment](/post/deploying-ai-dark-factory/) -- without quality gates, autonomous agents would degrade the codebase faster than humans can intervene.

## Rules Engine

Each project defines architectural constraints in `.sentrux/rules.toml`:

```toml
[constraints]
max_cycles = 5          # No more than 5 circular deps
max_cc = 30             # Functions max 30 complexity
max_file_lines = 500    # Files max 500 lines
no_god_files = true     # No files with >15 dependencies

[[layers]]
name = "core"
paths = ["src/core/*"]
order = 0

[[boundaries]]
from = "src/app/*"
to = "src/core/internal/*"
reason = "App must not depend on core internals"
```

Rules are checked on every PR. Violations block merge.

## Why This Matters

AI agents are powerful but limited. They cannot hold the big picture and small details simultaneously. Sentrux gives them the sensor they need to:

1. **See structure** -- Understand the codebase architecture
2. **Measure impact** -- Quantify the effect of each change
3. **Self-correct** -- Iterate when quality drops

This is the missing feedback loop. Compilers check syntax. Tests check behaviour. Linters check style. **Sentrux checks architecture.**

---

*Sentrux quality gates are now active on all Terraphim projects. PR checks include structural quality reports.*
