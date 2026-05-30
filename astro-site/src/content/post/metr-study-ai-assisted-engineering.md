---
title: "What the METR Study Actually Proves About AI-Assisted Engineering"
subtitle: "Developers were 19% slower with AI and believed they were 24% faster. The J-curve is real, and the organisations seeing 25-30% gains redesigned everything."
slug: "metr-study-ai-assisted-engineering"
description: "The METR randomised control trial found developers 19% slower with AI tools. Why the J-curve is real and frontier teams redesign everything, not just their tools."
tags: ["ai-engineering", "developer-productivity", "metr-study", "software-development"]
author: "Dr Alexander Mikhalev"
date: "2026-04-17"
draft: false
---

Developers were 19% slower with AI and believed they were 24% faster. The J-curve is real, and the organisations seeing 25-30% gains redesigned everything -- not just their tools.

## 1. The Study Nobody in AI Marketing Wants to Talk About

In 2025, METR ran a randomised control trial -- not a survey, not a vendor-commissioned benchmark -- on experienced open-source developers. Half used AI coding tools. Half did not. The researchers controlled for task difficulty, developer experience, and tool familiarity.

The result: developers using AI took **19% longer** to complete their tasks.

That finding alone would be inconvenient for the industry narrative. But the secondary finding is the one that should genuinely unsettle every engineering leader reading this. Those same developers **believed** the AI had made them 24% faster. They were wrong about the direction and wrong about the magnitude. The AI made them slower, and their self-assessment was off by 43 percentage points.

This is not a study about bad tools. This is a study about a broken mental model.

## 2. The J-Curve: Why AI Makes You Slower First

The METR result is not anomalous. It is the J-curve, and every adoption researcher worth reading has identified it.

When you bolt an AI coding assistant onto an existing workflow, productivity dips before it recovers. The shape looks like the letter J: down first, then up. The dip happens because the tool changes the work, but the workflow has not been redesigned around the tool. You are running a new engine through an old transmission. The gears grind.

In the METR trial, the grinding took specific forms. Developers spent their time evaluating AI suggestions that were almost right but not quite. They corrected code that looked plausible but contained subtle errors. They context-switched between their own mental model and the model's output. The generation speed of the AI was real. But the integration cost -- the cognitive overhead of supervising a fast, confident, occasionally wrong assistant -- more than cancelled it out.

GitHub Copilot illustrates this at scale. Twenty million users. Forty-two per cent market share. Lab studies show 55% faster code completion on isolated tasks. But in production, the picture is messier: larger pull requests, higher review costs, more security vulnerabilities introduced by generated code. One senior engineer put it precisely: "Copilot makes writing code cheaper but owning it more expensive."

## 3. The Self-Delusion Problem

The 24-point gap between perceived and actual productivity is not a curiosity. It is a structural danger.

If your organisation is measuring developer productivity by lines of code written or story points closed, you are almost certainly overestimating the impact of AI tooling. The METR study proves that self-reported productivity with AI is worse than useless as a metric -- it is actively misleading. You need outcome measures: time to production, defect rates, rollback frequency, incident response time.

## 4. What the Frontier Teams Actually Do Differently

The organisations reporting 25-30% productivity gains share one characteristic: they did not install a tool. They redesigned the system.

**StrongDM** runs a Level 5 ("dark factory") operation: three engineers, running since July 2024, shipping production Rust and Go code built entirely by agents. Their architecture includes scenario testing (not unit tests -- behavioural specifications stored outside the codebase as holdout sets), a Digital Twin Universe of simulated external services, and the Attractor agent -- an open-source coding agent that is just three markdown specification files. Their metric: "If you have not spent $1,000 per human engineer per day, your software factory has room for improvement."

**Anthropic** estimates functionally 100% of code at the company is AI-generated. Boris Churny, who leads the Claude Code project, has not personally written code in months.

**Cursor**: over $500 million ARR with a few dozen employees. Roughly $3.5 million revenue per employee, against a SaaS average of $600,000.

## 5. The Five Levels of Vibe Coding

Dan Shapiro's framework gives honest language:

**Level 0 -- Spicy Autocomplete.** AI suggests the next line. Human writes the code.

**Level 1 -- Coding Intern.** AI handles discrete, well-scoped tasks. Human reviews everything.

**Level 2 -- Junior Developer.** AI handles multi-file changes. 90% of developers who call themselves "AI native" operate here.

**Level 3 -- Developer as Manager.** Human directs AI and reviews at the feature or PR level. Most developers top out here because of the psychological difficulty of letting go.

**Level 4 -- Developer as Product Manager.** Human writes a specification, returns hours later to check tests.

**Level 5 -- Dark Factory.** Specs in, working software out.

## 6. The Brownfield Trap

Everything above assumes greenfield development. Most enterprise software is not greenfield. You cannot dark-factory your way through a legacy system. The specification for that system does not exist.

The migration path:
1. Use AI at Level 2-3 to accelerate existing work. Expect the J-curve dip.
2. Use AI to document what systems actually do.
3. Redesign CI/CD pipelines for AI-generated code at volume.
4. Shift new development to Level 4-5 patterns while maintaining legacy in parallel.

That path takes time. Anyone telling you otherwise is selling you something.

## 7. What We Did About It

The bottleneck is not the model, it is the specification.

We invested in three things: domain models as executable specifications, scenario-based testing as holdout sets (directly inspired by StrongDM), and specification quality as the primary metric.

The uncomfortable truth: most of our specifications were not good enough. They contained gaps that a human reader would fill with judgement. Machines do not have that layer. They build exactly what you describe.

## 8. The Uncomfortable Conclusion

The dark factory is real. StrongDM ships production software built entirely by agents. And most organisations are stuck at Level 2, getting measurably slower with AI tools they believe are making them faster.

The gap is not a technology gap. It is a people gap, a culture gap, an organisational gap. The machines have stripped away the camouflage. We are about to find out how good we actually are.
