---
title: "Terraphim RLM Skills: Local-First Recursive Language Model Orchestration"
subtitle: "Four native skills for Terraphim's Recursive Language Model, shipped in a day with capability-routed orchestration and no hardcoded model names."
slug: "terraphim-rlm-skills-local-first-orchestration"
description: "How we shipped four native RLM skills for local-first deterministic orchestration with capability-based routing and persistent knowledge graphs."
tags: ["rust", "llm", "local-first", "rlm", "terraphim"]
author: "Dr Alexander Mikhalev"
date: "2026-05-16"
draft: false
---

Shipped: four native skills for Terraphim's Recursive Language Model (RLM).

Local-first, capability-routed, no hardcoded model names. Built in a day with disciplined-research + disciplined-design, every step tracked in Gitea, every commit referencing an issue.

## The Four Skills

- **terraphim-rlm** -- wraps rlm_code, rlm_bash, rlm_query, rlm_context, rlm_snapshot, rlm_status
- **adf-orchestrate** -- adf-ctl trigger/status/cancel for overnight bigbox dispatch
- **kg-rlm-ingest** -- distil into role-scoped haystacks, verify via thesaurus cache flush
- **deterministic-rlm-review** -- multi-perspective swarm with explicit reconciliation

## Capability-Based Routing, Not Model Lock-In

The Capability enum has 11 variants: DeepThinking, FastThinking, CodeGeneration, SecurityAudit, Performance, and more. Prompts trigger the right tier documentation; terraphim_router picks the best provider with the CostOptimised strategy.

Tier documents are the single source of truth. Skill bodies never name a model.

This is a deliberate architectural choice. Model names change. Providers change. Pricing changes. But the *capability* your task needs -- deep analysis, fast code generation, security review -- is stable. By routing on capability rather than model name, the same skill works regardless of which provider offers the best model for that capability today.

## Three Execution Backends

All three are first-class citizens:

- **Local** -- default on Mac, fully supports rlm_code/bash/query/context/status. Honours timeout_ms and kill_on_drop. Only snapshots return NotSupported.
- **Docker** -- portable, container-level isolation, container-restart snapshots.
- **Firecracker** -- bigbox, strongest isolation, full VM state versioning.

The backend is selected by configuration, not by skill. The same skill runs locally on a developer laptop, in Docker on CI, and in a Firecracker microVM on the production server. No code changes between environments.

## What We Learned From Evaluation

Live vocabulary checking (no install required): negatives 8/8 perfect -- skill descriptions never falsely trigger unrelated skills.

Skill-creator run_loop trigger evaluation: 57-64% test pass rate, approximately 100% precision. Recall is capped because the runner does not install skills -- it measures whether vanilla Claude's response naturally uses Terraphim vocabulary.

The surprising finding: the same evaluation methodology limitation applies to both the repository's runner and skill-creator's run_loop.py. Neither tests installed-skill triggering. Both measure whether an unmodified AI assistant's response naturally references Terraphim concepts.

This makes them useful as regression guards but insufficient for answering "does my skill actually fire?" For that, you need interactive end-to-end testing with the skill installed.

In our interactive E2E test, all four skills triggered correctly:
- terraphim-rlm: called rlm_status first, used cargo metadata for cycle detection
- adf-orchestrate: identified correct adf-ctl invocation, asked for repo context
- kg-rlm-ingest: refused to fabricate KG content, suggested terraphim-agent sessions search instead
- deterministic-rlm-review: noted that "a confidence score on unread code would be theatre"

That last one is worth reflecting on. The review skill, when asked to review code it had not read, declined to produce a score. It is the correct behaviour. A confidence metric manufactured without evidence is not quality assurance -- it is theatre.

## Local vs Cloud RLM

Slate from randomlabs.ai shipped cloud RLM. We shipped local. Both approaches have merit.

Cloud RLM gives you immediate access to powerful infrastructure without local setup. It is the right choice when your data sovereignty requirements are modest and your latency tolerance is generous.

Local RLM gives you deterministic execution, persistent knowledge graphs, zero cloud round-trips, and complete data sovereignty. It is the right choice when your agents handle client intellectual property, when your knowledge graph contains proprietary domain models, or when you need reproducible execution for compliance.

The Terraphim stack combines local RLM orchestration with the terraphim_rlm crate in terraphim-ai. You get local-first deterministic orchestration with a persistent knowledge graph, and no data leaves your machine unless you explicitly choose to send it.

## Why This Matters

RLM -- Recursive Language Model -- is the pattern where an outer LLM plan decomposes into sub-calls that execute independently. Each sub-call can itself decompose further. The recursion terminates when a sub-task is simple enough to execute directly.

This pattern is powerful but dangerous without guardrails. An unbounded RLM can spiral: each decomposition spawns more sub-calls, each sub-call spawns more, and the budget explodes. Terraphim's RLM implementation enforces budget tracking, capability-based routing, and execution isolation.

The skills documented here are the interface layer. They translate between what an AI assistant wants to do ("decompose this task", "run this code", "query the knowledge graph") and what the RLM runtime actually does (budget allocation, sandbox creation, capability resolution).

Four skills. One day. Everything tracked, everything reproducible. That is the disciplined development process in action.
