---
title: "The Latency Problem Nobody in AI Wants to Discuss"
subtitle: "Real API benchmarks from connector validations. The AI industry has normalised mediocrity, and a UK government API is outperforming enterprise SaaS by 6x."
slug: "latency-problem-nobody-in-ai-discusses"
description: "Real-world API latency benchmarks showing Perplexity at 3,188ms, AWS Bedrock at 1,086ms, and Companies House at 121ms. Why the AI industry normalised slow APIs and what engineering discipline looks like."
tags: ["api-design", "latency", "performance", "ai"]
author: "Dr Alexander Mikhalev"
date: "2026-05-15"
draft: false
---

The AI industry has a latency problem, and we have collectively agreed to pretend it does not exist.

I ran connector validations across several APIs recently. Not synthetic benchmarks. Not health pings. Full authentication plus actual API operations -- the kind of work that happens every time your integration needs to verify it still works. The results tell a story the industry should find uncomfortable.

## The Numbers

| Service | Latency | What Is Being Measured |
|---------|---------|------------------------|
| Perplexity | 3,188ms | OAuth + LLM inference + likely web search |
| AWS Bedrock | 1,086ms | AWS SigV4 + Titan Express inference |
| Apollo | 792ms | API key + person enrichment |
| Zoho CRM | 656ms | OAuth + CRM user fetch |
| Companies House | 121ms | Basic auth + company profile fetch |

Let me be precise about what these numbers mean. We called Perplexity's research endpoint with "What is 1+1?" -- that likely triggered web search on top of inference. Bedrock got a simple "Say ok" prompt to Titan Express. Apollo did a person lookup. Companies House fetched a company profile. All included full authentication flows.

These are not unfair comparisons if you ask the right question: **How long does it take to verify your integration actually works?**

## The AI-to-AI Comparison

Strip away the SaaS APIs for a moment. Compare the two services doing LLM inference:

- Perplexity: 3,188ms
- AWS Bedrock: 1,086ms

Both authenticate. Both run inference. One is three times faster than the other.

Yes, Perplexity may include web search. But that raises a different question: if the only way to validate your integration is to trigger your most expensive operation, you have an API design problem. Well-architected APIs separate health checks from business logic. They give you a lightweight endpoint that says "yes, your credentials work, yes, the service is up" without burning inference cycles.

The absence of such an endpoint is a choice. It is a choice that says latency is not a priority.

## The Government Embarrassment

Here is the comparison that should keep enterprise SaaS engineers up at night:

- Companies House (UK government): 121ms
- Apollo (enterprise SaaS): 792ms
- Zoho CRM (enterprise SaaS): 656ms

All three operations are structurally similar: authenticate, fetch a record, return data. The government API -- not exactly known for cutting-edge engineering culture -- is five to six times faster than the enterprise alternatives.

This is not about complexity. Company profiles and CRM records are not fundamentally different data structures. This is about engineering discipline. Someone at Companies House decided their API should be fast, measured it, and kept it fast. That is the whole secret.

## Industry Standards Exist for a Reason

The benchmarks are not arbitrary:

- **Sub-100ms**: Excellent. Feels instantaneous.
- **100-300ms**: Best-in-class. Imperceptible delay.
- **Sub-1 second**: The non-negotiable baseline for modern APIs.
- **1-2 seconds**: Acceptable but noticeable. Users feel this.
- **2-5 seconds**: Tolerable. Impatience begins.
- **5+ seconds**: Unacceptable. Users leave.

Companies House hits "excellent." Bedrock barely misses "best-in-class." Perplexity does not clear "tolerable."

We have normalised mediocrity by making "it is doing AI" an acceptable excuse for any latency number. But Bedrock proves AI inference can happen in just over a second with proper architecture. The ceiling is not the technology. It is the engineering culture.

## Where the Time Goes

When an API takes three seconds to respond, the time goes somewhere. The usual suspects:

**Cold starts.** Serverless architectures that spin down to zero pay for it on every first request. This is a known tradeoff, and teams that care about latency either keep instances warm or accept the cost of always-on compute.

**Middleware bloat.** Every abstraction layer, every proxy, every "platform" feature adds milliseconds. Death by a thousand middleware.

**Lazy network architecture.** Chatty protocols, unnecessary round trips, connections that are not pooled, TLS handshakes that happen more often than they should.

**No latency budget.** If latency is not in your acceptance criteria, it never improves. Features ship when they work. They should ship when they work fast.

**The AI excuse.** "It is running a large language model" became a get-out-of-jail-free card for any performance number. But inference itself -- the actual matrix multiplications -- takes a predictable amount of time based on model size and hardware. Everything else is overhead, and overhead is engineering.

## The Cultural Problem

The AI boom created a permission structure for shipping slow software. When the core value proposition is "it does something magical," users tolerate waiting. They should not have to.

Bedrock's 1,086ms proves the point. AWS runs inference -- actual LLM inference -- behind their notoriously complex SigV4 authentication, and the whole operation completes in about a second. That is not because Amazon has magic hardware nobody else can access. It is because Amazon treats latency as a first-class engineering concern.

When latency is not a shipping blocker, it stays broken forever. Nobody files a bug that says "this works but it is slow." Slow becomes the baseline. The baseline becomes normal. Normal becomes defended.

## What Good Looks Like

Companies House at 121ms is what good looks like for a data fetch operation. That is not a simple service -- it is authenticating, querying what is presumably a substantial database, serialising the response, and returning it over the public internet. In 121 milliseconds.

For AI specifically, Bedrock at 1,086ms is the current bar. You can authenticate with enterprise-grade security, run inference on a capable model, and return a response in just over a second. That is the target every AI API should be measured against.

If your AI API takes three seconds for a simple query, the question is not "why is AI slow?" The question is "why is YOUR AI slow when others have proven it does not have to be?"

## The Path Forward

This is not a mystery to solve. Fast APIs come from teams that:

1. **Measure latency continuously.** P50, P95, P99. On every endpoint. With alerts.

2. **Set latency budgets.** "This endpoint must respond in under 500ms" as a hard requirement, not a nice-to-have.

3. **Design for lightweight validation.** Health endpoints that verify auth without triggering expensive operations.

4. **Treat cold starts as bugs.** Either keep instances warm or architect to avoid the problem.

5. **Audit the middleware stack.** Every proxy, every abstraction, every platform feature has a latency cost. Know what you are paying.

6. **Make latency a shipping blocker.** Features are not done when they work. They are done when they work fast.

The AI industry is young enough to fix this. But only if we stop accepting "it is doing inference" as an excuse for any performance number. The technology is not slow. The engineering culture is.

Speed is not a feature. It is engineering discipline made visible. And right now, most of the industry is showing us exactly how much discipline they do not have.

---

*Measurements taken December 2024. Your mileage may vary based on region, time of day, and load conditions. But the ratios tell the real story.*
