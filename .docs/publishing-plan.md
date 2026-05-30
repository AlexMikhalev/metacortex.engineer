# Metacortex Engineer Blog Publishing Plan

## Current State

### Existing Posts (34, imported from Hugo/Wowchemy)
All dated 2019-2022. Topics:
- **NLP/Redis**: 12 posts (RedisAI, RedisGears, knowledge graphs, BERT, NLP pipelines)
- **Data Science**: 5 posts (COVID/CORD19, data fusion, recommender systems)
- **Infrastructure**: 5 posts (Kubernetes, distributed storage, Ansible, cloud)
- **AI Ethics**: 2 posts (GitHub Copilot, ethics of creativity)
- **Soft Skills/Productivity**: 3 posts (agile, framing, soft skills)
- **General/Meta**: 7 posts (metacortex engineering, obsidian, etc.)

### Gap
No posts since 2022. No content covering Rust, AI agents, Terraphim, Zestic AI, or current work.

## New Posts Ready to Publish (~/cto-executive-system/blog-post-*.md)

| # | File | Title | Topic | Priority | Notes |
|---|------|-------|-------|----------|-------|
| 1 | blog-post-gpu-kg-vs-deterministic-automata.md | GPU-Accelerated KGs vs Deterministic Automata | Rust, AI, KG | HIGH | Core Terraphim tech story |
| 2 | blog-post-metr-study-ai-development.md | What the METR Study Actually Proves | AI, Research | HIGH | Contrarian take on AI productivity |
| 3 | blog-post-retrieval-approaches-ai-agents.md | The Retrieval Cost Spectrum | AI Agents, Architecture | HIGH | Unique technical angle |
| 4 | blog-post-dangerous-commands-guard.md | Dangerous Commands Guard | AI Safety, Rust | HIGH | Practical security content |
| 5 | blog-post-gitea-vs-github-ai-agents.md | Why We Chose Gitea Over GitHub | DevOps, AI Agents | MEDIUM | Thought leadership |
| 6 | blog-post-domain-model-quality-thread.md | The Domain Model as Quality Thread | Engineering, ZDP | MEDIUM | Zestic methodology |
| 7 | blog-post-llm-proxy-nobody-asked-for.md | The LLM Proxy Nobody Asked For | Rust, AI | MEDIUM | Pi-rust origin story |
| 8 | blog-post-metacognitive-self-correction.md | Teaching AI Agents Self-Correction | AI, Learning | MEDIUM | Terraphim learning system |
| 9 | blog-post-deploying-ai-dark-factory.md | Deploying an AI Dark Factory | DevOps, AI | LOW | Niche/technical |
| 10 | blog-post-gitea-robot-api.md | Gitea Robot API | DevOps | LOW | Follow-up to #5 |

### Additional Posts (~/cto-executive-system/blog/)
| # | File | Title | Topic | Priority |
|---|------|-------|-------|----------|
| 11 | 2026-02-23-teaching-ai-agents-self-correction.md | Teaching AI Agents Self-Correction | AI | MEDIUM (earlier draft of #8) |
| 12 | 2026-03-06-the-30-percent-problem.md | The 30% Problem | AI, Research | MEDIUM |
| 13 | verification-bottleneck-agi-economics.md | Verification Bottleneck AGI Economics | AI, Economics | MEDIUM |
| 14 | blog/posts/teaching-ai-assistants-pagerank-prioritization.md | PageRank Prioritization | AI, DevOps | LOW (subset of #10) |

### Twitter Thread to Expand
| # | File | Title | Topic | Priority |
|---|------|-------|-------|----------|
| 15 | blog-post-rlm-skills-thread-2026-05-16.md | Terraphim RLM Skills Landed | AI, Terraphim | LOW (thread format, needs rewrite) |

## Publishing Schedule

### Phase 1: Anchor Posts (Week 1-2)
Establish the new voice and technical authority. 3 posts spaced 3-4 days apart.

1. **"What the METR Study Actually Proves About AI-Assisted Engineering"** (#2)
   - Broadest appeal (AI productivity is hot topic)
   - Contrarian angle: "developers were 19% slower"
   - Sets up credibility for AI methodology posts

2. **"GPU-Accelerated Knowledge Graphs vs Deterministic Automata"** (#1)
   - Core technical differentiator
   - Bridges old Redis/KG content with new Rust work
   - Links naturally to existing KG posts

3. **"The Retrieval Cost Spectrum: Why Your AI Agent's Memory Architecture Matters"** (#3)
   - Deep technical content
   - Positions Terraphim as thought-through architecture
   - Links to existing NLP pipeline posts

### Phase 2: Practical & Safety (Week 3-4)
Show real-world engineering, not just theory.

4. **"Dangerous Commands Guard: Why Prompt-Level Security Is Not Enough"** (#4)
   - Practical AI safety
   - Appeals to anyone building AI agents
   - Good for Hacker News / Reddit

5. **"The LLM Proxy Nobody Asked For"** (#7)
   - Engineering war story
   - Shows Rust expertise
   - Links to pi-rust/Terraphim

6. **"Teaching AI Agents to Learn from Their Mistakes"** (#8, skip #11 as duplicate)
   - Metacognitive learning
   - Directly relevant to TruthForge and Terraphim

### Phase 3: Methodology & Ecosystem (Week 5-8)
Build the Zestic AI narrative.

7. **"The Domain Model as Quality Thread"** (#6)
   - ZDP methodology introduction
   - Enterprise architecture audience

8. **"Why We Chose Gitea Over GitHub for AI Agent Coordination"** (#5)
   - DevOps/thought leadership
   - Gitea community will amplify

9. **"The 30% Problem"** (#12)
   - Research analysis
   - Broader AI industry commentary

10. **"Verification Bottleneck and AGI Economics"** (#13)
    - Big-picture thinking
    - Forward-looking, positions as visionary

### Phase 4: Technical Deep Dives (Month 3+)
11. **"Deploying an AI Dark Factory"** (#9)
12. **"Gitea Robot API"** (#10) (or merge with #5)
13. **RLM Skills** (#15, rewritten from thread)

## Content Guidelines

### Frontmatter Template
```yaml
---
title: "Title Here"
subtitle: "One-line summary"
slug: "url-friendly-slug"
description: "Meta description for SEO, under 160 chars"
tags: ["tag1", "tag2", "tag3"]
author: "Dr Alexander Mikhalev"
date: "2026-XX-XX"
draft: false
---
```

### Author Bio
Use "Dr Alexander Mikhalev, CTO & Head of AI at Zestic AI" in bylines.

### Internal Linking Strategy
- Link new posts to existing Redis/NLP posts where relevant
- Cross-link between new posts (retrieval -> KG, dangerous commands -> metacognitive)
- Link to projects section (Terraphim AI, TruthForge) from relevant posts

### SEO Notes
- Each post gets unique meta description (under 160 chars)
- Tags should reuse existing tag vocabulary where possible
- Slug format: lowercase-hyphenated, matches existing convention

## Conversion Checklist (per post)
1. Read source file from ~/cto-executive-system/
2. Add Astro frontmatter (title, subtitle, slug, description, tags, author, date)
3. Convert any non-markdown formatting to standard markdown
4. Remove Twitter thread numbering (for #15)
5. Add internal links to existing posts and projects
6. Set description for SEO
7. Place in `astro-site/src/content/post/`
8. Build and verify locally
9. Deploy to R2
10. Verify live URL returns 200

## Topics for Future Posts (Not Yet Written)
- Astro migration from Hugo (this project itself)
- Rust for AI: why we bet on it
- The Zestic Development Process (6D lifecycle)
- Privacy-first AI: building without cloud dependencies
- Context Engineering as a discipline
