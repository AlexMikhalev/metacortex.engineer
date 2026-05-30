---
title: "Teaching AI Agents to Learn from Their Mistakes: From FINAL Bench to Production Self-Correction"
subtitle: "FINAL Bench proves models know when they are wrong. Terraphim-agent ships the infrastructure to actually fix it."
slug: "teaching-ai-agents-self-correction"
description: "How the FINAL Bench declarative-procedural gap inspired Terraphim's learning capture system: persistent failure memory, Aho-Corasick query expansion, and the MetaCog self-correction scaffold."
tags: ["ai", "self-correction", "learning", "agents", "terraphim"]
author: "Dr Alexander Mikhalev"
date: "2026-04-17"
draft: false
---

FINAL Bench proves models know when they are wrong. Terraphim-agent ships the infrastructure to actually fix it.

## The Apologise-and-Repeat Loop

Your agent runs `cargo build --features nonexistent`. It fails. The agent apologises and tries again. Same command, same failure. Third attempt, still the same mistake. Three rounds of increasingly verbose contrition, zero actual correction.

The model knows the command failed. It can even articulate why. But knowing and fixing are different operations, and current agent architectures have almost no infrastructure for the second one.

## What FINAL Bench Measured

FINAL Bench evaluated nine state-of-the-art models across 100 tasks spanning 15 domains. It measured Metacognitive Accuracy (MA) -- whether a model can correctly identify when it might be wrong -- and Error Recovery (ER) -- whether the model actually corrects the error.

Across all nine models:

- **MA = 0.694** -- models are decent at recognising uncertainty
- **ER = 0.302** -- models are poor at actually fixing errors
- **57% gap** between declarative awareness and procedural correction

Models with high MA and low ER produce "silent failures" -- they sound humble, acknowledge limitations, and then produce uncorrected errors anyway. The model's verbal humility becomes a mask for procedural incompetence.

The MetaCog scaffold (generate, self-review, revise) produces a mean improvement of +14.05 points. But **94.8%** of that improvement comes from the revision phase. Self-review barely moves the needle. Revision is where the value lives.

Claude Opus 4.6 ranks last at baseline and fifth with the scaffold -- a 20.13-point gain, the highest scaffold receptivity. The models that seem worst at single-pass generation are the best at self-correction when given the structure to do it.

## Terraphim's Learning Capture System

The Learning Capture System works as a PostToolUse hook. When any command fails, the hook fires automatically:

```
$ cargo build --features nonexistent
  --> error[E0557]: feature `nonexistent` is not a feature

[PostToolUse hook fires]
  1. Parse: command="cargo build --features nonexistent", exit_code=101
  2. Redact: scanning for secrets -- none found
  3. Store: .terraphim/learnings/2026-02-23-cargo-build-features.md
  4. KG query: "cargo features" -> suggests: check Cargo.toml [features] section
```

The stored learning is a plain Markdown file with YAML frontmatter. Not a database. Markdown is human-readable, git-trackable, and requires no additional infrastructure. Learnings travel with the project.

The components:

**Secret redaction.** Regex-based stripping of AWS keys, database connection strings, API tokens before storage.

**KG-expanded search.** Aho-Corasick automata expand queries across domain synonyms. Searching for "cargo features" also matches "build flags", "compile options", "feature flags".

**Correction annotations.** After fixing a failure, the correction is stored as a procedure:

```bash
terraphim-agent learn correct learning_20260223_143012 \
    --correction "Feature name is 'full' not 'nonexistent'. Run: cargo build --features full"
```

This is the critical design decision. Corrections are stored as procedures, not descriptions. This directly addresses the 57% declarative-procedural gap.

## The MetaCog Skill

**Phase 1: Capture.** The PostToolUse hook. When a command fails, the error is parsed, redacted, stored, and the knowledge graph is queried for related patterns.

**Phase 2: Self-Review.** Query the learning store for prior occurrences:

```bash
$ terraphim-agent learn diagnose "cargo build --features nonexistent"

## Diagnostic Context
- Prior occurrences: 3 (2 project, 1 global)
- Known correction: "Check Cargo.toml, feature name is 'full'"
- Related patterns: cargo feature flag errors (5 total)
- Confidence: high
```

**Phase 3: Revise.** Apply the correction, re-run, verify:

```bash
$ terraphim-agent learn auto-correct learning_20260223_143012

## Applying Correction
- Original: cargo build --features nonexistent
- Correction: cargo build --features full
- Result: SUCCESS (exit_code=0)
- Correction verified and stored
```

The key insight: storing corrections as procedures addresses the declarative-procedural gap directly. The model does not need to "understand" why the feature flag was wrong. It needs the specific procedure: replace `nonexistent` with `full`.

## The Bottleneck Is Infrastructure, Not Models

The FINAL Bench evidence shows that self-correction capability exists in the models already. Claude Opus 4.6 gained 20 points when given the structure to self-correct. The bottleneck is not the model. The bottleneck is the infrastructure around the model.

The MetaCog scaffold is three API calls: generate, review, revise. It requires a hook that captures failures, a store that persists them, and a query mechanism that retrieves them when the same pattern recurs. That is what terraphim-agent provides.

The bottleneck to reliable AI agents is not better models. It is giving models the infrastructure to learn from their mistakes. That infrastructure does not need to be complex. It needs to exist.
