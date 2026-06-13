# Blog Publishing Plan -- Batch 2

## Source Material Inventory

### Already Published (48 posts)
See `astro-site/src/content/post/` for full list. All 13 posts from `~/cto-executive-system/` and the privacy-first AI post are live.

### Candidate Posts from `~/projects/terraphim/terraphim-ai/blog/`

| # | File | Title | Topic | Lines | Priority | Notes |
|---|------|-------|-------|-------|----------|-------|
| 1 | `2026-02-16-native-hook-support.md` | Native Hook Support | Learning capture, hooks | 230 | HIGH | Overlaps with "Teaching AI Agents Self-Correction" -- MERGE or differentiate |
| 2 | `2026-02-20-learning-via-negativa.md` | Learning via Negativa | Failure learning, KG | 284 | HIGH | Unique angle: via negativa philosophy applied to AI learning |
| 3 | `2026-02-16-zvec-vs-terraphim-comparison.md` | zvec vs Terraphim | Semantic search comparison | 298 | MEDIUM | Alibaba's neural vectors vs deterministic automata |
| 4 | `2026-04-29-sentrux-quality-gates.md` | Sentrux Quality Gates | CI/CD, ADF quality | 204 | HIGH | New feature announcement, links to ADF post |
| 5 | `announcing-github-runner.md` | Terraphim GitHub Runner | Firecracker CI/CD | 326 | MEDIUM | Product announcement, needs de-emoji |
| 6 | `2026-02-16-multi-haystack-roles-grepapp.md` | Multi-Haystack Roles | GrepApp, search | 177 | LOW | Niche feature, better as section in retrieval post |

### Candidate Posts from `~/projects/terraphim/` (standalone files)

| # | File | Title | Topic | Lines | Priority | Notes |
|---|------|-------|-------|-------|----------|-------|
| 7 | `blog-api-latency-ai-industry-v2.md` | The Latency Problem Nobody Discusses | API latency benchmarks | 113 | HIGH | Contrarian, data-driven, links to retrieval cost spectrum |
| 8 | `context_graph_manifesto.md` | Context Graph Manifesto | Knowledge graphs, context engineering | 78 | MEDIUM | Thought leadership on context engineering |
| 9 | `Rust_binary_optimisation.md` | Rust Binary Optimisation | Rust, Docker, musl | 55 | LOW | Technical tip, combine with another post |
| 10 | `terraphim_graph_embeddings_build_system.md` | Graph Embeddings Build System | Firecracker, VM snapshots | 802 | LOW | Very niche, Layerfile migration research |

### Promotion Material (Social/Drafts -- NOT for blog)

| File | Type | Notes |
|------|------|-------|
| `twitter-thread-v1.8.1.md` | Twitter thread | v1.8.1 release announcement, rewrite as short post? |
| `twitter-draft.md` | Twitter draft | GitHub Runner announcement, overlaps with #5 |
| `reddit-draft.md` | Reddit draft | GitHub Runner for r/rust, overlaps with #5 |
| `twitter-thread-api-latency-v2.md` | Twitter thread | Latency thread, source material for #7 |

### NOT Recommended for Blog

| File | Reason |
|------|--------|
| `FPF-Spec.md` (37,578 lines) | Technical specification, not a blog post |
| `blog-api-latency-ai-industry.md` (v1) | Superseded by v2 |
| `terraphim_graph_embeddings_build_system.md` | Research notes, not structured for blog |

---

## Recommended Publishing Plan (8 posts)

### Phase 1: High-Impact Technical Posts (Week 1)

**1. The Latency Problem Nobody in AI Wants to Discuss** (#7)
- Source: `blog-api-latency-ai-industry-v2.md`
- Why: Data-driven, contrarian, links naturally to existing retrieval cost spectrum post
- Audience: Engineering leads, API architects
- Conversion: Make it concrete with real numbers from connector validations

**2. Learning via Negativa: How Terraphim Remembers What You Keep Getting Wrong** (#2)
- Source: `2026-02-20-learning-via-negativa.md`
- Why: Unique philosophical angle (via negativa) applied to AI failure learning
- Audience: AI practitioners, knowledge engineers
- Cross-link: "Teaching AI Agents Self-Correction" (already published)
- Differentiation: Previous post covers FINAL Bench + MetaCog scaffold. This one covers the *philosophy* of learning from failures via negativa -- what NOT to do

**3. Sentrux Quality Gates: Closing the Feedback Loop on AI-Generated Code** (#4)
- Source: `2026-04-29-sentrux-quality-gates.md`
- Why: Product announcement, links to ADF post and domain model quality thread
- Audience: CI/CD engineers, DevOps leads
- Cross-link: "Deploying an AI Dark Factory" (already published)

### Phase 2: Comparison & Product Posts (Week 2)

**4. zvec vs Terraphim: Two Paths to Semantic Search** (#3)
- Source: `2026-02-16-zvec-vs-terraphim-comparison.md`
- Why: Alibaba's neural approach vs deterministic automata -- tech comparison
- Audience: Search engineers, AI architects
- Cross-link: "GPU KGs vs Deterministic Automata" (already published)
- Note: Differentiate from GPU KG post -- that one covers NVIDIA RAPIDS. This covers zvec specifically.

**5. Announcing Terraphim GitHub Runner** (#5)
- Source: `announcing-github-runner.md`
- Why: Product announcement, Firecracker + LLM for CI/CD
- Audience: DevOps, platform engineers
- Changes needed: Remove emoji, remove exclamation marks, tone down hype per PRODUCT.md guidelines

**6. The Context Graph: Why RAG Is Not Enough** (#8)
- Source: `context_graph_manifesto.md` + expand
- Why: Thought leadership on context engineering vs RAG vs GraphRAG
- Audience: AI architects, CTOs
- Cross-link: "Retrieval Cost Spectrum" (already published)
- Changes needed: Expand from 78 lines to full blog post, add Terraphim-specific architecture

### Phase 3: Technical Deep Dives (Week 3)

**7. Rust Binary Optimisation for Minimal Docker Images** (#9)
- Source: `Rust_binary_optimisation.md`
- Why: Practical Rust tip, complements the LLM proxy and ADF posts
- Audience: Rust developers, DevOps
- Changes needed: Expand from 55 lines, add benchmarks, before/after image sizes

**8. Firecracker VM Snapshots: Building Layerfile-Performance Build Systems in Rust** (#10)
- Source: `terraphim_graph_embeddings_build_system.md`
- Why: Unique technical content, Firecracker + Rust = niche expertise
- Audience: Systems engineers, CI/CD architects
- Changes needed: Extract the architecture story from the research notes, add Mermaid diagram

---

## Posts to Skip / Defer

- **Multi-Haystack Roles** (#6): Niche feature, better as a section in the existing retrieval cost spectrum post
- **Native Hook Support** (#1): Overlaps heavily with "Teaching AI Agents Self-Correction" -- the via negativa post (#2) covers the learning philosophy instead
- **FPF-Spec**: Not blog material
- **Social drafts**: Rewrite as short posts or keep as social-only content

## Summary

| Phase | Posts | Est. words |
|-------|-------|------------|
| Phase 1 (Week 1) | Latency, Via Negativa, Sentrux Quality Gates | ~4,000 |
| Phase 2 (Week 2) | zvec comparison, GitHub Runner, Context Graph | ~4,500 |
| Phase 3 (Week 3) | Rust binary opt, Firecracker snapshots | ~3,000 |
| **Total** | **8 posts** | **~11,500** |

Site would grow from 48 to 56 posts.
