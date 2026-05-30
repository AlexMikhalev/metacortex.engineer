---
title: "Why We Chose Gitea Over GitHub for AI Agent Coordination"
subtitle: "Rate limits, the Robot API, package registries, and the PageRank algorithm that made our agents self-organising."
slug: "gitea-vs-github-ai-agents"
description: "Why we moved our AI agent coordination layer from GitHub to self-hosted Gitea: rate limits, PageRank prioritisation, privacy, and package registries."
tags: ["gitea", "github", "ai-agents", "pagerank", "self-hosted", "devops"]
author: "Dr Alexander Mikhalev"
date: "2026-04-17"
draft: false
---

Rate limits, the Robot API, package registries, and the PageRank algorithm that made our agents self-organising.

## The Night the Agents Stopped Working

At 11pm on a Tuesday in March, five autonomous agents stopped picking up tasks. No errors. No crashes. No alerts. They just sat idle, polling an API that had started returning `403 Forbidden` with increasing regularity.

GitHub's secondary rate limit had kicked in. We had exceeded 5,000 authenticated requests per hour across our agent fleet. Five agents, each polling issues every 30 seconds, each checking assignments, each posting progress comments, each querying the dependency state of their repository -- that adds up to roughly 600 API calls per agent per hour. Five agents. 3,000 calls. Then the cron-driven triage jobs. Then the CI status checks. Then the package publishes.

We hit the ceiling before midnight.

The fix was simple in the short term: stagger the polling intervals, add exponential backoff, cache more aggressively. We deployed those changes the next morning. But the underlying problem remained. We were building an autonomous agent system -- what we internally call the AI Dark Factory -- on a platform designed for humans clicking through web interfaces. GitHub was never built for machines that never sleep.

This is the story of why we moved our entire agent coordination layer to Gitea, what we lost in the process, and why the trade was worth it.

## What Agents Need From a Code Platform

Before comparing platforms, it helps to understand what autonomous agents actually do with a code hosting service. This is not the same as what humans do.

Humans visit a repository, read issues at their leisure, assign labels based on judgement, and maybe pick up a task when they feel like it. Agents do none of that. An agent's interaction with a code platform is mechanical and relentless:

1. **Query for available work** -- every 30-120 seconds, around the clock
2. **Claim a task** -- assign itself, add a label, post a comment
3. **Create a branch** -- git operations via the API
4. **Post progress** -- comments on the issue, sometimes every few minutes
5. **Open a pull request** -- create PR, request reviewers, set labels
6. **Respond to review** -- push fixes, update the PR, comment back
7. **Close the issue** -- merge, close, move on to the next task
8. **Publish artefacts** -- push built packages to a registry

A single agent completing one task can generate 50-100 API calls over its lifecycle. Now multiply that by five to ten agents running concurrently, 24 hours a day, across multiple repositories. The numbers stop looking like normal developer usage and start looking like a denial-of-service attack.

This is the core tension. GitHub is optimised for human-scale interaction. Agents operate at machine scale. The platform assumptions -- rate limits, OAuth flows designed for browser redirects, pricing per human user, public-by-default visibility -- all assume the consumer is a person sat at a keyboard.

## The Rate Limit Problem Is Structural

GitHub's rate limits are not a bug. They are a deliberate design choice that makes perfect sense for human users and breaks down entirely for agent workloads.

The primary rate limit for authenticated requests is 5,000 per hour. For a human developer, that is generous. You would need to make 83 API calls per minute, every minute, for an hour, to hit it. No human does that.

Five autonomous agents with 30-second polling intervals do it before lunch.

The secondary rate limit is more insidious. It applies to content-changing requests: creating issues, posting comments, pushing commits. GitHub does not publish exact thresholds for this one. You discover it empirically, usually at 11pm on a Tuesday, when your agents silently stop working.

We could have paid for GitHub Enterprise. At $21 per user per month, that is $21 per agent per month. Ten agents across two projects: $420 per month just for the agents to have API access. GitHub Enterprise raises rate limits but does not eliminate them. And it introduces a different problem: every agent's activity, every issue it creates, every comment it posts, every package it publishes -- all of it lives on Microsoft's infrastructure, subject to Microsoft's terms of service, visible to Microsoft's compliance systems.

For some organisations, that is fine. For an AI consultancy building autonomous agents that work on client code, it was not fine.

## PageRank: Why Agents Cannot Prioritise Without It

Rate limits were the incident that forced the decision. But the deeper architectural reason was prioritisation.

GitHub has labels. You can tag an issue `priority: high` or `priority: critical`. A human triager sets those labels based on experience, context, and gut feeling. An agent staring at 200 open issues with manually-assigned priority labels has no reliable way to decide what to work on next. The labels are stale the moment they are applied. Dependencies between issues are invisible to flat label-based sorting.

What agents need is a mathematical answer to a specific question: "Which issue, if I resolve it, unblocks the most downstream work?"

That question has a well-known answer. PageRank. The same algorithm Google used to rank web pages by link importance, applied to issue dependency graphs instead of hyperlink graphs. An issue's score rises when many other issues depend on it. An issue that blocks nothing scores low. An issue that blocks ten other issues scores high.

GitHub has no native PageRank for issues. You can build it externally -- pull the issue graph via the API, compute PageRank locally, store the scores. But that means maintaining a separate service, syncing state with GitHub, and paying API calls for the privilege of calculating something the platform should calculate for you.

Gitea 1.26.0 ships PageRank as a first-class feature. The Robot API exposes three endpoints:

```bash
# Rank all issues by dependency impact
gtr triage --owner terraphim --repo project

# Filter to unblocked issues an agent can start immediately
gtr ready --owner terraphim --repo project

# Expose the full dependency graph for planning
gtr graph --owner terraphim --repo project
```

The triage endpoint returns issues ranked by PageRank score. The ready endpoint filters to issues with no blockers. An agent calls both at the start of each work cycle, picks the highest-scoring unblocked issue, and gets to work. No human triager. No stale labels. No guessing.

The algorithm runs in approximately 50 milliseconds for a repository with 1,000 issues. It caches results with a 5-minute TTL. The cache hit rate is over 95% because dependency graphs change slowly compared to API query frequency.

## Privacy: Why Your Agent Conversations Should Not Live on Microsoft Servers

Every comment an agent posts on a GitHub issue is stored on Microsoft's infrastructure. Every issue description, every code review comment, every CI log -- all of it. For a team building AI agents that work on client code, this creates a category of risk that has nothing to do with rate limits or pricing.

Our agents discuss architectural decisions in issue comments. They debate implementation approaches. They post error logs, stack traces, and configuration details. They sometimes include snippets of client code in their progress reports. None of this is information we want sitting on a third-party platform, subject to that platform's data processing terms.

Gitea runs on our hardware. The database is our PostgreSQL instance. The logs are our logs. When an agent posts a comment analysing a security vulnerability, that comment lives on a server we control, behind a VPN we administer, in a jurisdiction we chose.

The `FORCE_PRIVATE = true` setting in our Gitea configuration is not a convenience flag. It is a business requirement.

## The Migration: What We Lost and What We Gained

Migration was not painless. We lost things.

**GitHub Actions CI/CD.** We had years of workflow definitions. Gitea Actions is compatible with the GitHub Actions syntax, and most workflows transferred with find-and-replace changes, but not all. We estimate it took two engineer-days per repository to migrate CI pipelines.

**Pull request review UX.** GitHub's code review interface is genuinely better than Gitea's. The inline commenting, the suggestion feature, the review summary -- Gitea's PR review is functional but less polished.

**Network effects.** GitHub is where the open-source community lives. Our public projects still have GitHub mirrors. But the primary development happens on Gitea.

What we gained:

**Zero rate limits.** Our Gitea instance handles 100+ concurrent agent requests without throttling. It is a 40MB compiled Go binary running on PostgreSQL. We have never seen a self-imposed rate limit fire.

**PageRank prioritisation.** Agents pick the right task every time. Not the task with the loudest label, but the task that unblocks the most downstream work. This is the single biggest improvement to agent productivity we have measured.

**Self-hosted package registries.** Eight registry types (npm, Cargo, Conda, PyPI, NuGet, Maven, Go, Composer), unmetered, private by default.

**Privacy by default.** Every repository, every issue, every comment, every package -- all on hardware we control.

**Cost.** Gitea is free. When your "users" include ten autonomous agents and a handful of human developers, the monthly bill difference is material.

## When GitHub Is Still the Right Choice

If you have two agents, not ten, GitHub's rate limits are manageable. If your agents work on open-source projects, GitHub is where the community is. If you do not have infrastructure capacity, self-hosting has a cost in operational overhead. And if PageRank-based prioritisation is not important to you -- if manual labels and human triagers are working fine -- then the Robot API's main selling point does not apply.

## The Honest Summary

We moved to Gitea because we were building an AI Dark Factory -- autonomous agents that pick up tasks, write code, submit pull requests, and close issues without human intervention. GitHub's rate limits, pricing model, and public-by-default architecture were designed for human developers, not for machines that never stop making API calls.

The migration cost us CI pipeline migration effort, a slightly worse PR review interface, and some open-source visibility. It saved us rate-limit-induced outages, per-seat pricing for non-human users, and the operational overhead of maintaining a separate coordination layer.

Sometimes the right answer is not a better API client. Sometimes it is a different platform.
