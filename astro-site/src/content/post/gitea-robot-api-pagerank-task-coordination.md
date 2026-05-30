---
title: "We Tried Three Task Coordination Tools Before Realizing Gitea Already Had the Answer"
subtitle: "Gitea 1.26.0 ships a Robot API with PageRank-based issue prioritisation. Here is why it took us four attempts to get here."
slug: "gitea-robot-api-pagerank-task-coordination"
description: "How we replaced three bespoke coordination systems with Gitea's Robot API and PageRank-based issue prioritisation for AI agent workflows."
tags: ["gitea", "ai-agents", "pagerank", "devops", "coordination"]
author: "Dr Alexander Mikhalev"
date: "2026-04-17"
draft: false
---

Gitea 1.26.0 ships a Robot API with PageRank-based issue prioritisation. Here is why it took us four attempts to get here.

---

## How We Got Here: Three Wrong Answers Before the Right One

I want to be honest about something before we get into the technical details. The Gitea Robot API is the fourth attempt at solving multi-agent task coordination. The first three were wrong. Not because they were badly built -- they were solid open-source projects by talented developers. They were wrong *for our problem*. Each one taught us something, and each one got removed from our stack.

Understanding why they did not fit matters more than understanding why the current solution works.

### Attempt 1: beads -- SQLite in Your Git Repo

The first instinct was local-first. We adopted beads, Steve Yegge's SQLite-based issue tracker that stores metadata in `.beads/` directories committed alongside your code. Every agent had its own local database. You ran `bd ready --json` to see unblocked tasks, `bd create --title "X" --priority=2` to file issues, `bd dep add` to wire up dependencies.

It felt clean. Local. Fast. No server dependency. Every repo carried its own task state.

It was also completely invisible to every other agent and every other human on the team. You had to commit `.beads/` alongside your code. Priorities were manual -- P0 through P4, assigned by gut feeling. When five agents worked across eight repos, nobody had a coherent view of what mattered most. The dependency graph existed, but only locally, per-repo, with no global picture.

Local-first is the right default for data. It is the wrong default for coordination.

### Attempt 2: beads_rust -- Faster, Same Problem

We then switched to beads_rust, Jeffrey Emanuel's Rust port of beads. Faster SQLite operations. Better CLI ergonomics (`br` instead of `bd`). Smaller binary. Type safety throughout.

Same fundamental architecture. Same local-only limitation. Same manual priority assignment. Same fragmented view across repos.

A faster tool does not fix a structural mismatch. This is the most seductive engineering trap -- performance improvements on a design that does not fit your problem feel like progress. They are not. beads_rust solved a problem we did not have (SQLite performance on tiny datasets) while leaving untouched the problem we did have (no shared state, no intelligent prioritisation).

The lesson applies broadly: when evaluating tools, validate the architecture against your constraints before benchmarking the implementation.

### Attempt 3: MCP Agent Mail -- Overengineering the Coordination Layer

Having learned that local-only fails for multi-agent coordination, we swung to the opposite extreme. We deployed MCP Agent Mail, Jeffrey Emanuel's MCP-based coordination server, on a dedicated machine accessible over Tailscale VPN. Full agent-to-agent messaging. TTL-based file reservation with exclusive locking. Session lifecycle management. Real-time inboxes.

It was architecturally sophisticated. It was also a maintenance burden that depended on a specific server being up, a specific VPN being connected, and a complex lease mechanism not expiring at the wrong moment. We had adopted a bespoke coordination service that duplicated capabilities already present in every issue tracker since 2005 -- but with more moving parts and fewer users who understood it.

MCP Agent Mail solved real problems. But it solved them by adding infrastructure instead of leveraging infrastructure we already had.

### The Insight: Your Issue Tracker Already Knows

The breakthrough was embarrassingly simple. We already ran Gitea. Gitea already had issues, comments, assignments, labels, and an API. Every agent already authenticated against it. Every human already read it.

What Gitea lacked was one thing: it could not tell you which issue to work on next based on dependency impact. It had no concept of "this issue blocks four other issues, so fix it first."

That is a single algorithm. PageRank. The same algorithm Google used to rank web pages by link importance. Applied to issues instead of URLs, dependencies instead of hyperlinks. A node's score rises when many other nodes depend on it.

We did not need a local SQLite database. We did not need a Rust rewrite. We did not need a bespoke MCP coordination server. We needed three API endpoints and a well-understood graph algorithm bolted onto the tool we were already using.

### What We Traded Away (On Purpose)

Honesty demands acknowledging what we lost:

- **No TTL-based file reservations.** Branch isolation handles this. If two agents need the same files, they work on branches and merge through PRs. The conflict resolution mechanism is called "git." It has been battle-tested.
- **No real-time push messaging.** Agents poll via `gtr list-issues --owner O --repo R --state open`. Polling with a 30-second interval is fine. Your agents are not high-frequency traders.

These are real losses. We made them consciously because the alternative -- maintaining a separate coordination server -- cost more than the gaps. Pre-commit and pre-push guards, notably, are not among the losses -- those still run via git hooks and the judge system, independent of the coordination layer.

### The Command Migration

For anyone walking the same path, here is what changed:

| Before (beads / Agent Mail) | After (Gitea + PageRank) |
|---|---|
| `br ready --json` | `gitea-robot ready --owner O --repo R` |
| `br create --title "X" --priority=2` | `gtr create-issue --owner O --repo R --title "X"` |
| `br close ID` | `gtr close-issue --owner O --repo R --index IDX` |
| `register_agent(project_key)` | Not needed -- `GITEA_TOKEN` identifies the agent |
| `file_reservation_paths(exclusive=true)` | Branch isolation + comment: "RESERVED: paths" |
| `send_message(thread_id)` | `gtr comment --owner O --repo R --index IDX --body "message"` |
| `fetch_inbox` | `gtr list-issues --owner O --repo R --state open` |

Every command on the right side uses a tool that already existed. We wrote zero coordination infrastructure. We wrote one Go binary (`gitea-robot`) that calls three new API endpoints.

The rest of this post covers those endpoints, the algorithm, and how to deploy it. But the lesson above is the one worth remembering: the best infrastructure is the infrastructure you do not build.

---

## What is the Robot API?

The Robot API is a set of endpoints purpose-built for AI agents and automation tools to interact with Gitea issues. Unlike traditional issue APIs that return flat lists sorted by date or manual priority, the Robot API understands dependency relationships between issues and calculates their relative importance using PageRank.

### The Problem: Agents Cannot Prioritise

An AI agent staring at 200 open issues has no way to decide which one matters most. Sort by date? Meaningless. Sort by manual priority label? Stale the moment it was assigned. The agent needs to know: which issue, if resolved, unblocks the most downstream work?

Humans struggle with this too. But agents face it on every single task selection cycle, with no intuition to fall back on.

### The Solution: Graph-Based Prioritisation for Agents

The Robot API gives agents three capabilities:
1. **Triage** -- rank all issues by dependency impact (PageRank score)
2. **Ready** -- filter to only unblocked issues an agent can start immediately
3. **Graph** -- expose the full dependency structure for planning

---

## Key Features

### 1. PageRank-Powered Triage

The `/api/v1/robot/triage` endpoint returns issues ranked by their importance in the dependency graph:

```bash
curl https://git.terraphim.cloud/api/v1/robot/triage \
  -H "Authorization: token $TOKEN" \
  --data-urlencode "owner=terraphim" \
  --data-urlencode "repo=project"
```

**Response:**
```json
{
  "quick_ref": {"total": 15, "open": 12},
  "recommendations": [
    {
      "id": 42,
      "title": "Refactor authentication system",
      "pagerank": 0.85,
      "status": "open"
    },
    {
      "id": 38,
      "title": "Update API documentation",
      "pagerank": 0.72,
      "status": "open"
    }
  ],
  "project_health": {
    "avg_pagerank": 0.45,
    "max_pagerank": 0.85
  }
}
```

An agent reads the `recommendations` array top-to-bottom. The first item is always the highest-leverage work available.

### 2. Ready Task Identification

The `/api/v1/robot/ready` endpoint shows issues that have no blockers and are ready to work on:

```bash
gitea-robot ready --owner terraphim --repo project
```

An agent calls this before starting work. If `ready_issues` is empty, there is nothing to do -- all remaining work is blocked. The agent can report this and wait, rather than picking up blocked work and stalling.

### 3. Dependency Graph Visualisation

The `/api/v1/robot/graph` endpoint returns the complete dependency graph. Agents use this for planning. A coordinating agent can partition the graph across worker agents, assigning independent subgraphs to avoid conflicts.

---

## The PageRank Algorithm

We adapted Google's PageRank algorithm for issue prioritisation:

1. **Nodes = Issues**: Each issue is a node in the graph
2. **Edges = Dependencies**: "Issue A blocks Issue B" creates a directed edge
3. **PageRank Calculation**: Issues that block many other issues get higher scores
4. **Damping Factor**: 0.85 (standard PageRank damping)
5. **Iterations**: 100 (ensures convergence)

```
PR(A) = (1-d)/N + d * (PR(B)/L(B) + PR(C)/L(C) + ...)
```

PageRank handles cycles, converges quickly, and produces interpretable scores in the 0.0-1.0 range.

---

## Agent Workflows

### 1. Agent Task Selection

```python
import requests

def pick_next_task(owner, repo, token):
    base = "https://git.terraphim.cloud/api/v1/robot"
    headers = {"Authorization": f"token {token}"}

    ready = requests.get(f"{base}/ready",
        headers=headers,
        params={"owner": owner, "repo": repo}
    ).json()["ready_issues"]

    if not ready:
        return None

    return max(ready, key=lambda i: i["page_rank"])
```

Two API calls. One decision. The agent picks the highest-impact unblocked task and starts working.

### 2. Multi-Agent Coordination

When multiple agents work the same repo, each one claims work through Gitea assignments. No custom coordination protocol needed.

```bash
# Agent claims the highest-impact unblocked issue
gtr edit-issue --owner O --repo R --index 42 --add-labels "status/in-progress" --add-assignees "agent-alpha"

# Agent communicates progress via issue comments
gtr comment --owner O --repo R --index 42 --body "Implemented auth refactor. PR incoming. Refs #42"

# Agent closes when done
gtr close-issue --owner O --repo R --index 42
```

---

## Performance

- **PageRank calculation**: ~50ms for 1000 issues
- **Cache hit rate**: 95%+ with 5-minute TTL
- **API response time**: <100ms for triage endpoint
- **Memory overhead**: ~10MB for issue graph

---

## Conclusion

Three custom systems. Two rewrites. One MCP server. All replaced by three API endpoints and a graph algorithm that has been public knowledge since 1998.

What you get:
- **Focus on high-impact issues** -- fix what unblocks the most work
- **Eliminate manual triage** -- PageRank calculates priority from dependency structure
- **AI-agent native** -- built for automation, not bolted on after the fact
- **Private by default** -- security-first design with audit logging
- **Self-hosted** -- your data, your infrastructure, your rules

The simplest tool that solves the actual problem beats the sophisticated tool that solves the wrong one. We learned that the hard way, three times over.
