---
title: "Deploying an AI Dark Factory: 10 Bugs in 48 Hours and What They Taught Us"
subtitle: "Two ADF instances, ten production bugs, one merged Rust PR. A field report from the first 48 hours of autonomous AI agents closing real issues."
slug: "deploying-ai-dark-factory"
description: "A field report from deploying autonomous AI agent factories that pick up Gitea issues, write code, submit pull requests, and close bugs without human intervention."
tags: ["ai-agents", "rust", "devops", "production-engineering"]
author: "Dr Alexander Mikhalev"
date: "2026-04-17"
draft: false
---

Two ADF instances, ten production bugs, one merged Rust PR. A field report from the first 48 hours of autonomous AI agents closing real issues.

## The Ambition

On April 17, 2026, we deployed two autonomous AI agent factories -- "AI Dark Factory" instances, or ADF -- onto a single server. The goal: have self-directed agents pick up Gitea issues, write code, submit pull requests, and close bugs without human intervention. Not a demo. Not a proof of concept. Real production work on real repositories.

**Odilo ADF** manages four agents on the `zestic-ai/odilo` project. **Digital Twins ADF** manages five agents on the `terraphim/digital-twins` Rust workspace (ten crates). Both run as systemd services on a dedicated server, coordinated through Gitea with PageRank-based task prioritisation.

The core reconciliation loop is a `tokio::select!` that races three event sources: a scheduler (cron triggers), nightwatch (monitoring alerts), and a tick interval (periodic polling). Tick fires every 60 seconds. Mention polling runs on every second tick (120 seconds). Cron runs hourly during working hours (`0 1-9 * * *`). The routing engine uses terraphim-automata -- Aho-Corasick matching over a knowledge graph -- to match agent tasks to the right model tier.

Three routing tiers exist: Planning (priority 80) for coordinators, Implementation (priority 50) for developer agents, and Review (priority 40) for reviewers and QA. A Dangerous Commands Guard provides pre-execution hooks to prevent any model from running destructive operations, regardless of what the LLM decides to do.

That is the system we designed. Here is what actually happened when we turned it on.

---

## Bugs 1-3: The Ones That Nearly Killed Us

### Bug 1: 106% CPU from a Stale Binary

The first ADF instance started and immediately consumed 106% of a CPU core. A busy loop. The binary on the server had been compiled on April 7. Ten days of development had fixed the loop, but nobody had rebuilt the binary.

This is the most basic deployment mistake: the code was correct, the deployment was stale. We rebuilt from the latest `main` on April 17 and the CPU dropped to normal idle.

Lesson: if you deploy binaries, the build step must be part of the deployment pipeline, not a manual step that happened "at some point."

### Bug 2: The Routing Engine Silently Discarded CLI Tool Overrides

This one was subtle and it took careful log analysis to find. Our knowledge graph routing correctly identified that Anthropic models should use the `claude` CLI tool. The config said `claude`. The logs showed the routing decision. But the agents kept invoking `opencode` instead.

The routing engine was discarding the CLI tool override from the KG match and falling back to the default. The fix required a Rust code change -- PR #592 on Gitea, #819 on GitHub. It was reviewed and merged the same day.

This bug matters because it exposed a design flaw: the routing engine had two sources of truth (KG match and default config) and the merge logic silently favoured the default. No error. No warning. Just wrong behaviour.

The fix was straightforward once diagnosed:

```rust
// Before: KG tool override silently lost
let tool = kg_match.tool.unwrap_or(config.default_tool);

// After: explicit precedence, logged when override applies
let tool = if let Some(ref t) = kg_match.tool {
    tracing::info!(tool = %t, "KG routing override for CLI tool");
    t.clone()
} else {
    config.default_tool.clone()
};
```

### Bug 3: Model Names Version-Pinned to IDs That Expire

Our configuration had model names like `claude-3-5-sonnet-20241022`. Version-pinned model IDs. When Anthropic updates a model, the old ID either stops working or routes to a degraded version.

We switched to aliases: `haiku`, `sonnet`, `opus`. These resolve to whatever the latest version is on the provider side. The same principle applies to OpenAI and other providers. Pin your behaviour requirements, not your model IDs.

This was a configuration fix, not a code change. But it is the kind of thing that causes silent degradation: the agent still works, just worse, and you do not notice until you compare outputs side-by-side.

---

## Bugs 4-7: The Configuration Minefield

### Bug 4: Developer Agent Matched the Review Tier

Our routing taxonomy uses keyword matching. The developer agent template contained the word "review" in its description -- something like "review code changes before committing." The Aho-Corasick automaton matched "review" and routed the developer agent to the review tier (priority 60) instead of the implementation tier (priority 50).

The fix: lower the review tier priority from 60 to 40, below the implementation tier at 50. Now "review" matches review tier, but implementation tier wins on priority when both match.

```toml
# routing_scenarios/adf/implementation_tier.md
priority = 50

# routing_scenarios/adf/review_tier.md
priority = 40  # was 60 -- lowered to avoid developer false match
```

This bug reveals a fundamental tension in keyword-based routing: natural language descriptions are ambiguous. The Aho-Corasick engine is exact and fast, but it has no semantic understanding. We could move to embedding-based routing, but that adds latency and complexity. For now, careful taxonomy design and priority ordering is sufficient.

### Bug 5: Missing compound_review Section Crashes the Binary

The Rust binary that runs the orchestrator expected a `compound_review` section in the TOML config. Our config generation script did not emit one. The binary panicked on startup with a deserialisation error.

Fix: add the section to the config generation. This is a missing-required-field bug, and it points to a deeper problem: the Rust binary's config schema and the Python config generator are not validated against each other. We need a shared schema or at minimum a config validation step before deployment.

### Bug 6: Missing nightwatch Section -- Same Pattern

Same story, different section. The binary required a `nightwatch` section even if nightwatch was not configured. The fix: always emit a minimal nightwatch section.

```toml
[nightwatch]
enabled = false
interval_secs = 300
```

After bugs 5 and 6, we added a config validation step to the deployment script. The script now generates the TOML, parses it back with `tomllib`, and verifies all required sections exist before copying to the server.

### Bug 7: systemd Environment Variable Expansion Does Not Work

This one was frustrating because the systemd documentation suggests it should work. Our service file had:

```ini
[Service]
Environment=GITEA_TOKEN=${GITEA_TOKEN}
```

systemd does not expand shell variables in `Environment=` directives. The literal string `${GITEA_TOKEN}` was passed to the process. The ADF binary received `${GITEA_TOKEN}` as the token value, which obviously failed authentication with Gitea.

The fix was to embed the token directly in the TOML config file:

```toml
[gitea]
url = "https://git.terraphim.cloud"
token = "actual-token-value-here"
```

This is not ideal from a secrets management perspective. The proper solution is `EnvironmentFile=` pointing to a file with restricted permissions, or systemd's `LoadCredential=`. We will migrate to `EnvironmentFile=` in the next iteration. For the initial deployment, the TOML file has `0600` permissions owned by the service user.

---

## Bugs 8-10: The Subtle Ones

### Bug 8: Quickwit Schema `tokenized: false` Is Invalid

Our Quickwit log index schema had text fields marked as `tokenized: false`. Quickwit does not support that syntax. The correct form is:

```yaml
- name: agent_name
  type: text
  indexed: true
  tokenizer: raw
```

This meant the index was not created correctly, and agent logs were silently dropped. No error in the ADF binary -- it would post to the Quickwit ingest endpoint and receive a non-200 response, but the orchestrator treated log ingestion as best-effort and continued.

The fix: correct the schema and recreate the index. We lost about two hours of agent logs from the initial deployment window.

### Bug 9: argparse Default None vs Pydantic str

Our Python config generation used argparse with `--review-gate` defaulting to `None`. The Pydantic model expected a `str`. When the argument was not provided, `None` was passed to Pydantic, which rejected it.

```python
# Before: argparse default None, Pydantic expects str
parser.add_argument("--review-gate", default=None)

# After: explicit default matching Pydantic type
parser.add_argument("--review-gate", default="reviewer")
```

This is a type boundary bug. Python's dynamic typing makes it easy to pass `None` where a string is expected, and it only fails at validation time. Pydantic caught it, which is good. The fix is to align the defaults across the boundary.

### Bug 10: Meta-Coordinator Posted Mentions Without Agent Names

The meta-coordinator agent would post comments like:

```
@adf: please handle this task.
```

The mention handler requires the format `@adf:<agent-name>`, e.g. `@adf:developer`. Without the agent name, the handler silently ignored the mention. The developer agent was never dispatched.

This was the last bug we found, and the most consequential. The meta-coordinator is the brain of the operation -- it decides which agent should handle which issue. If its mentions are silently ignored, the entire system appears to work (no errors, logs look normal) but no agents are dispatched.

The fix: add a MANDATORY section to the meta-coordinator's prompt template:

```toml
[prompt.mandatory]
mention_format = """
When dispatching work, you MUST use the exact format:
  @adf:developer -- for implementation tasks
  @adf:reviewer -- for code review
  @adf:qa -- for testing

Mentions without an agent name (e.g. @adf: ) will be silently ignored.
"""
```

After this fix, the meta-coordinator started dispatching correctly, and the Digital Twins developer agent picked up issue #9 within the next cron cycle.

---

## What Actually Worked

Despite ten bugs in 48 hours, the system closed real issues.

**Odilo ADF:**
- Closed issue #35 (hardcoded path bug) and #36 (u8 overflow)
- Created PRs #38 and #40
- Developer agent ran multiple cron cycles autonomously

**Digital Twins ADF:**
- Closed issue #3 (Linear twin, 12/12 SDK tests passing)
- Closed issue #6 (smoke test)
- Created PR #8
- Validated Solr SDK tests: 14/14 passing
- Fixed a HubSpot DashMap deadlock that was blocking issue work

Both instances have all 10 provider probes reporting healthy. The routing engine, once the bugs were fixed, correctly assigns planning-tier models (opus, gpt-5.4, glm-5) to coordinators, implementation-tier models (sonnet, kimi, glm-5-turbo) to developers, and review-tier models (haiku, gpt-5.4-mini) to reviewers and QA.

The PageRank-based issue prioritisation works as designed. When the meta-coordinator runs on its cron schedule, it queries Gitea for the highest-priority unblocked issue, checks if an agent is available, and dispatches with the correct mention format. The dependency graph means agents work on the right issues in the right order.

---

## The Deployment Script

After debugging these ten issues across two deployments, we wrote a setup script so nobody has to do this manually again. The script handles:

```bash
uv run python adf_setup.py \
  --project digital-twins \
  --repo terraphim/digital-twins \
  --coordinator-model "zai-coding-plan/glm-5" \
  --agents "developer,reviewer,qa" \
  --cron-schedule "0 1-9 * * *" \
  --working-dir /home/alex/projects/zestic-ai/digital-twins \
  --init \
  --apply
```

The `--init` flag generates project context (a `.docs/summary.md` from the repository) that agents use to understand the codebase. The `--apply` flag writes the generated files. Without `--apply`, it runs in dry-run mode for preview.

The script:
1. Generates the orchestrator TOML with all required sections (compound_review, nightwatch)
2. Uses model aliases, not version-pinned IDs
3. Sets review tier priority to 40 (below implementation at 50)
4. Defaults review_gate to "reviewer" (not None)
5. Includes the mandatory mention format in meta-coordinator templates
6. Validates the generated TOML with `tomllib` before writing
7. Generates the Quickwit index schema with correct field definitions

Three commits captured the fixes: `b77671c1` (5 deployment-discovered bugs), `1c36d60d` (model aliases), and `73849826` (review tier priority and review_gate default).

---

## Lessons: What We Would Do Differently

**1. Config schema contract between Rust binary and Python generator.**

Bugs 5 and 6 (missing required sections) should not be possible. The Rust binary's config struct and the Python generator need a shared schema, or at minimum the generator needs to validate against the binary's expected shape. We are adding a JSON Schema file that both sides reference.

**2. End-to-end smoke test before declaring "deployed."**

We should have run a full dispatch cycle -- meta-coordinator picks an issue, mentions a developer, developer picks it up, posts a comment -- before walking away from the terminal. The silent failures (bug 10 especially) would have been caught in minutes instead of hours.

**3. systemd secrets management from day one.**

Bug 7 (environment variable expansion) is a well-known systemd gotcha, and we should have used `EnvironmentFile=` from the start. Embedding secrets in config files is a shortcut that becomes a liability.

**4. Structured logging with required fields.**

The orchestrator logged routing decisions, but not in a structured way that made debugging easy. After bug 2 (routing override lost), we added explicit structured logging for routing overrides. This should have been there from the beginning.

**5. The mention format is a protocol, not a prompt.**

Bug 10 revealed that the mention handler is effectively a message-passing protocol between agents. Protocols need schemas, not natural language instructions in a prompt template. We are formalising the mention format as a schema with validation.

**6. Model aliases, always.**

Bug 3 was predictable. Version-pinned model IDs are fragile. Aliases that resolve to the current best model on the provider side are the only sane default.

**7. The first deployment of any autonomous agent system is debugging, not operating.**

We planned for a deployment. What we got was 48 hours of production debugging. This is normal for the first deployment of a complex distributed system. The lesson is to plan for it: schedule the deployment when you have time to debug, not when you need the system running.

---

## The Honest Assessment

Ten bugs in 48 hours is not a failure. It is the expected cost of deploying a distributed autonomous system for the first time. The important metric is not the bug count -- it is that both ADF instances are now running autonomously, closing real issues, submitting real PRs, and doing it without human intervention.

The Odilo developer agent fixed a u8 overflow and a hardcoded path. The Digital Twins developer agent validated 14 Solr SDK tests and fixed a DashMap deadlock. These are real production fixes, not toy problems.

The AI Dark Factory is operational. It is fragile, it needed ten patches to get there, and the configuration surface is still too large. But it works. And now we have a setup script and a bug catalogue that means the third deployment will take hours, not days.

The dark factory metaphor is apt. In manufacturing, a dark factory runs without lights because nobody works there. Our dark factory runs without direct human oversight because the agents handle the work cycle themselves. But just like a real factory, someone has to set up the machines, calibrate the sensors, and fix the assembly line when it jams. That is what the first 48 hours were: setting up the machines.
