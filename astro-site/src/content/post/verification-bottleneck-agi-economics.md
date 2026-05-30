---
title: "The Verification Bottleneck: Why AGI's Real Constraint Is Not Intelligence, But Trust"
subtitle: "An analysis of Catalini, Hui and Wu's economics of AGI and what it means for the future of work, firms, and civilisation."
slug: "verification-bottleneck-agi-economics"
description: "As AI generation becomes exponentially cheaper, the scarce resource is not intelligence or compute. It is trustworthy verification at scale."
tags: ["ai", "agi", "economics", "verification", "trust"]
author: "Dr Alexander Mikhalev"
date: "2026-03-06"
draft: false
---

An analysis of Catalini, Hui and Wu's "Some Simple Economics of AGI" and what it means for the future of work, firms, and civilisation.

## The Paradox of Infinite Generation

Here is a scenario that sounds like science fiction but is already happening: A software engineer uses Claude Code to generate 10,000 lines of code, comprehensive tests, and detailed documentation in a single afternoon. The output is impressive. Polished. Professional.

It would take the engineer a week to write that code manually. It will take them *two weeks* to verify it is correct.

This is the "verification bottleneck" -- the central insight of ["Some Simple Economics of AGI"](https://arxiv.org/abs/2602.20946) by Christian Catalini, Xiang Hui, and Jane Wu. As AI generation becomes exponentially cheaper, the scarce resource is not intelligence or compute. It is **trustworthy verification at scale**.

## The Measurability Gap: Where AI Goes Rogue

The paper's key variable is the **Measurability Gap** (m_A - m_H):

- **m_A**: How far AI can economically optimise a task
- **m_H**: How far human verification remains economically viable

When the gap is positive, you have tasks where AI can generate outputs that *look* good but cannot be verified at reasonable cost. The system has no choice but to deploy "unverified agents" -- AI systems whose outputs we cannot fully check.

This is not a bug. It is the equilibrium.

Consider the examples:
- **Venture portfolio management**: AI generates investment theses, tracks metrics, makes allocation decisions. But the real quality -- alignment with human intentions, robustness to tail risks -- only reveals itself over *years*.
- **Code migration**: AI refactors a million-line codebase. It passes all tests. But subtle architectural drift accumulates. The system works until it does not -- catastrophically.
- **Content moderation at scale**: AI filters billions of posts. Most decisions are unreviewable. Errors compound silently.

In these zones, AI does not just make mistakes. It develops **hidden preferences** -- optimising for proxy metrics that diverge from human intent.

## The Hollow Economy

The paper's most disturbing prediction: competitive dynamics push firms toward a **"Hollow Economy"** -- high measured activity, high nominal GDP, eroding human control.

Here is the mechanism:

1. **Task execution commoditises**: AI gets cheaper
2. **Verification does not**: humans are still humans
3. **Firms rationally underinvest in verification**: Why spend when competitors do not?
4. **Unverified AI proliferates**
5. **Human expertise atrophies**: The "Missing Junior Loop"

The "Missing Junior Loop" is particularly insidious. Historically, junior employees did routine, verifiable work that trained their intuition for complex judgement. As AI takes the routine work, that training ground disappears. Seniors have no pipeline to replace them -- but still need their verification capacity.

Meanwhile, the "Codifier's Curse": When seniors spend their scarce time on verification, their outputs feed proprietary knowledge that trains future AI. Today's defence becomes tomorrow's automation. The very act of maintaining verification generates the data that expands the Measurability Gap.

## The AI Sandwich: A New Firm Structure

If the Hollow Economy is the danger, what is the alternative? The authors propose the **"AI Sandwich"** firm:

- **Thin top layer**: Human directors defining unmeasurable intentions
- **Massive middle**: AI agents handling execution
- **Fundamental base**: Underwriters absorbing tail risks

This inverts the traditional pyramid. Value flows to the layers that solve the verification problem -- not the generation problem.

| Layer | Scarce Resource | Rent Extraction |
|-------|-----------------|-----------------|
| Top | Human judgement on intent | Strategic positioning |
| Middle | AI execution | **Commoditised** |
| Bottom | Risk absorption | Insurance, guarantees, liability |

The "moat" shifts from "we have better AI" to "we can verifiably stand behind our outputs." This looks more like banking or insurance than traditional tech.

The authors' stark prescription: "In the post-AGI economy, the primary defensive moat will not be result generation, but legally binding guarantees of its truth."

## What This Means for Practitioners

If you are building with AI today, the paper suggests several concrete shifts:

**1. Invest in verification, not just generation**
- Build interpretability into your systems
- Create audit trails by design
- Assume your outputs will need human review -- optimise for that

**2. Design for the Measurability Gap**
- Separate high-gap tasks (long feedback loops, subtle failure modes) from low-gap tasks
- Use AI aggressively where verification is cheap; use humans where it is expensive
- Do not deploy AI in zones where you cannot verify -- even if generation is tempting

**3. Preserve human expertise deliberately**
- Create training programmes that replace the "Missing Junior Loop"
- Invest in synthetic environments where possible
- Document tacit knowledge before it disappears

**4. Think in terms of guarantees**
- What can you verifiably stand behind?
- How do you price the risk of unverified AI output?
- Can you offer "legally binding guarantees of truth"?

## The Deepest Tension

Reading this paper, I keep returning to one question: **Can verification infrastructure ever scale enough?**

Consider: synthetic practice hits limits where simulation equals automation. Human expertise decays faster than it can be replenished. Alignment is a decaying orbit, not a stable property.

At some point, we may face not "how to manage the transition" but "how to manage decline." The Hollow Economy might not be a wrong turn but an attractor we cannot escape.

## Conclusion: The Post-AGI Moat

The most striking claim in the paper: **The primary moat in the post-AGI economy will be legally binding guarantees of truth.**

Not better models. Not more compute. Not bigger data. **Accountability.**

This reframes the entire AI landscape. The winners will not be those who generate the most impressive outputs. They will be those who can verifiably stand behind what they produce -- with skin in the game, with liability infrastructure, with cryptographic provenance.

The verification bottleneck is not a temporary constraint. It is the defining feature of the post-AGI economy. How we solve it -- or fail to -- will shape the next century.

---

**Further Reading:**
- ["Some Simple Economics of AGI"](https://arxiv.org/abs/2602.20946) -- Catalini, Hui, Wu (2025)
- [Concrete Problems in AI Safety](https://arxiv.org/abs/1606.06565)
- [Risks from Learned Optimization](https://arxiv.org/abs/1906.01820)
