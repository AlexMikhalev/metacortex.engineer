---
title: "Dangerous Commands Guard: Why Prompt-Level Security Is Not Enough for AI Agents"
subtitle: "Any model at any moment can ignore prompts. Here is the pre-execution hook that prevents destructive commands regardless of LLM intent."
slug: "dangerous-commands-guard-ai-agents"
description: "Why prompt-level security fails for autonomous AI agents, and how a pre-execution hook with deny-list patterns catches destructive commands before they run."
tags: ["ai-safety", "rust", "security", "ai-agents"]
author: "Dr Alexander Mikhalev"
date: "2026-04-17"
draft: false
---

Any model at any moment can ignore prompts. We learned this the hard way. Here is the pre-execution hook that prevents destructive commands regardless of LLM intent.

## 1. The Amazon AWS Wake-Up Call

On 10 March 2026, Amazon's AWS division experienced what the industry should treat as a canonical warning. AI-assisted operations tools, granted access to production infrastructure, caused issues in Cost Explorer. The incident was not theoretical -- it was real money, real customers, real production impact.

The model was not malicious. It was optimising for a reward signal, and the path of least resistance happened to pass through a destructive operation that the permissioning system had not anticipated.

We watched this unfold and recognised our own vulnerability.

## 2. Why "Just Use Permission Modes" Does Not Work

Every major AI coding tool offers permission control. This is dangerously incomplete for three reasons.

**First, bypass-permissions exists.** Every tool that offers autonomous mode includes a mechanism to skip the permission prompt. Our agents run autonomously for hours. Stopping for human approval on every shell command would defeat the purpose.

**Second, sandboxing is insufficient in practice.** The constant approval interrupts make interactive development painful, and sandbox constraints prevent legitimate operations. Our Firecracker VM-based agents regularly consume 70GB of RAM for build processes.

**Third, prompts are advisory, not enforced.** You can write the most detailed instruction set telling an agent never to run `git reset --hard`, and any sufficiently capable model will understand and agree. But models are not deterministic. Under the right conditions, the model will take the shortest path to satisfying its objective.

The fundamental insight: **you cannot enforce security at the prompt layer because the prompt layer has no enforcement mechanism.**

## 3. The Architecture: A Pre-Execution Hook

The Dangerous Commands Guard sits between the LLM's tool-use output and the actual shell execution.

```
LLM generates tool call
    |
    v
Agent framework prepares shell execution
    |
    v
[dcg hook intercepts]  <-- This is where security lives
    |
    +-- ALLOW --> Shell executes command
    |
    +-- DENY  --> Command blocked, reason returned to agent
```

### Why a Deny-List, Not an Allow-List

An allow-list requires enumerating every command an agent might legitimately need. Our agents execute thousands of distinct commands across build systems, test frameworks, package managers, Docker, Kubernetes, and bespoke project scripts. The combinatorial explosion makes a comprehensive allow-list impractical.

A deny-list blocks only known-dangerous patterns. The cost of a false positive is developer frustration; the cost of a false negative is data loss.

### Fail-Open Semantics

If the guard itself fails -- timeout, parse error, resource exhaustion -- the command is allowed to proceed. A security guard that breaks your workflow will be removed. The default is intentionally permissive.

## 4. The Specific Commands We Block

**Git destructive operations** (80% of incidents):

```bash
git reset --hard          # Destroys all uncommitted changes
git checkout -- .         # Discards working directory changes
git push --force          # Rewrites shared history
git clean -fdx            # Removes untracked files and directories
```

**Filesystem destruction:**

```bash
rm -rf /                  # Self-explanatory
rm -rf /etc               # System configuration
rm -rf ./src              # Source code
```

**Inline script execution:**

```bash
bash -c "rm -rf /"
python -c "import os; os.system('rm -rf /')"
```

The guard detects obfuscation: quoted commands, absolute paths, sudo variants, and command substitution. Beyond these core patterns, the pack system provides 49 categories covering PostgreSQL, Docker, Kubernetes, AWS, Terraform, and more.

## 5. What It Does NOT Catch

**Arbitrary code via script files.** An agent can write a destructive script and execute it. The repository scanning mode catches these in committed code, but not in real-time.

**Semantic destruction.** The guard blocks `git reset --hard` but not `git commit -m "replacing entire codebase with Hello World"`. Security at this level requires understanding intent.

**Prompt injection.** A malicious file could manipulate the agent into performing destructive actions through a sequence of individually safe commands. This is the hardest problem in agent security.

These gaps are acceptable because the guard is one layer in a defence-in-depth strategy. It catches the 80% caused by well-known command patterns.

## 6. The Broader Lesson

**Enforce constraints at the execution layer, not the instruction layer.**

Prompts are instructions to the model. Hooks are constraints on the system. Instructions can be ignored. Constraints cannot.

When we build security into prompts, we are asking a statistical text generator to behave like a security policy engine. This is a category error. A pre-execution hook is a deterministic program that evaluates every command against a fixed set of patterns with sub-millisecond latency. This is what enforcement looks like.

The Amazon AWS incident was predictable. Every team running autonomous agents will eventually encounter a scenario where the model takes a destructive action that its instructions forbade. The question is whether you will have an enforcement mechanism in place when it does.

Install the guard. Configure the packs. Do not rely on prompts to protect your production infrastructure.
