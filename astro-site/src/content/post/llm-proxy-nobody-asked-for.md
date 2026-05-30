---
title: "The LLM Proxy Nobody Asked For (And Why We Built It Anyway)"
subtitle: "When OpenRouter could not do keyword routing and fallback drills, we wrote our own in Rust."
slug: "llm-proxy-nobody-asked-for"
description: "Building a Rust LLM proxy with Aho-Corasick keyword routing, multi-provider fallback chains, and deliberate failure injection to prove it works."
tags: ["rust", "llm", "proxy", "routing", "infrastructure"]
author: "Dr Alexander Mikhalev"
date: "2026-04-17"
draft: false
---

When OpenRouter could not do keyword routing and fallback drills, we wrote our own in Rust. Here is what it does.

## The Rate Limit That Started It

A few days into running our AI coding assistant at full tilt, the OpenAI Codex Pro plan rate limit hit. Not gently -- it hit like a brick wall in the middle of a productive session.

The obvious answer was OpenRouter. Except OpenRouter does not do keyword-based routing. It does not let you define fallback chains with explicit provider ordering. And it certainly does not let you simulate outages on purpose to verify your fallback works.

We needed three things:
1. Route requests based on the content of the prompt, not just the model ID
2. Fail over transparently from one provider to the next
3. Prove both work, on demand, with real failure injection

## Architecture: A Rust Proxy That Routes Before It Forwards

The proxy sits between the AI coding tool and the outside world. It exposes OpenAI-compatible and Anthropic-compatible endpoints. Everything downstream is the proxy's problem.

```toml
[router]
default = "openai-codex,gpt-5.2-codex|zai,glm-5"
think = "openai-codex,gpt-5.2|minimax,MiniMax-M2.5|zai,glm-5"
long_context = "openai-codex,gpt-5.2|zai,glm-5"
strategy = "fill_first"

[[providers]]
name = "openai-codex"
api_base_url = "https://api.openai.com/v1"
models = ["gpt-5.2", "gpt-5.2-codex", "gpt-5.3"]

[[providers]]
name = "zai"
api_base_url = "https://api.z.ai/api/paas/v4"
models = ["glm-5", "glm-4.7"]

[[providers]]
name = "minimax"
api_base_url = "https://api.minimax.io/anthropic"
transformers = ["anthropic"]
models = ["MiniMax-M2.5"]
```

The `fill_first` strategy means "use the first provider in the chain that responds." The client never knows which provider actually served the request.

## The Keyword Routing Trick

The `think` scenario is triggered by keywords in the prompt. When someone writes "think step by step about this architecture," the proxy matches the keywords and routes to the `think` chain instead of `default`.

The matching uses Aho-Corasick string matching from the `terraphim-automata` crate -- the same algorithm we use in our knowledge graph. Overhead is in the microsecond range.

The taxonomy lives in plain markdown files:

```markdown
# MiniMax Keyword Routing

route:: minimax, MiniMax-M2.5
priority:: 100
synonyms:: minimax, minimax keyword, minimax route, m2.5
```

Real production evidence from our logs:

```text
Routing decision provider=minimax model=MiniMax-M2.5 scenario=Pattern("minimax_keyword_routing")
Routing decision provider=openai-codex model=gpt-5.2 scenario=Pattern("think_routing")
Routing decision provider=openai-codex model=gpt-5.2-codex scenario=Default
```

Three requests, three different routing decisions, all transparent to the client.

## Fallback Drills: Simulating Outages on Purpose

Having a fallback chain is theatre until you prove it works under real failure conditions.

We test by deliberately breaking the primary provider: add `127.0.0.1 chatgpt.com` to `/etc/hosts`, send a request, and watch it fall through to Z.ai.

```text
Primary target failed, attempting fallback target
next_provider=zai
```

The response comes back. The client never sees an error. We run these drills periodically because providers change endpoints, deprecate models, and introduce new rate limits without warning.

## API Compatibility Lessons

The hardest part was not routing or fallback. It was API format mismatches.

**Z.ai (GLM-5)** is genuinely OpenAI-compatible. Worked on the first try.

**MiniMax** is not OpenAI-compatible. It is Anthropic-compatible -- different endpoint structure, different headers, different message format. We had to write transformers that convert between formats depending on which provider the request is being forwarded to.

The edge cases around streaming, tool calls, and system messages across these two formats are full of small incompatibilities that only surface under real usage.

## The Cost Economics

Z.ai and MiniMax offer models with competitive performance at substantially lower cost per token than the major Western providers. The tradeoff is reliability and latency. These providers have less geographic redundancy.

This is exactly why fallback chains matter. Route to the cheaper provider when it is up, fall back to the reliable provider when it is not. The proxy lets us have both.

## When to Build Your Own vs Use a Service

**Use a service if:** one or two providers, basic failover, low traffic, no content-based routing.

**Build your own if:** keyword routing, genuinely different API formats, provable fallback through failure injection, you already have the building blocks.

We fell into the second category. The proxy cost roughly two days of engineering time, built on crates we already maintained.

## What We Got Wrong

The `/etc/hosts` hack for failure injection is embarrassing. It works but requires sudo and affects the entire machine. We also underestimated how often provider APIs change silently. Z.ai changed their response format twice in three months without updating documentation.

If you run a proxy like this, budget time for ongoing compatibility maintenance. It is not a build-once-and-forget project.
