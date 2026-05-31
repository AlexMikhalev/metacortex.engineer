---
title: "Privacy-First AI: Why We Built an AI Assistant That Never Calls Home"
subtitle: "58 Rust crates, zero cloud dependencies, Aho-Corasick matching that runs in a browser. The architecture of a local-first AI system."
slug: "privacy-first-ai-building-without-cloud-dependencies"
description: "How Terraphim AI achieves privacy-first AI by moving knowledge graphs instead of data, using deterministic automata, embedded databases, and WASM deployment."
tags: ["privacy", "local-first", "rust", "wasm", "ai", "terraphim"]
author: "Dr Alexander Mikhalev"
date: "2026-05-31"
draft: false
---

58 Rust crates, zero cloud dependencies, Aho-Corasick matching that runs in a browser. The architecture of a local-first AI system.

## The Problem With Cloud AI

The standard AI product architecture is straightforward: upload your data to our servers, we run it through our models, we send results back. Every major AI assistant works this way. ChatGPT, Claude, Gemini -- all of them process your data on infrastructure you do not control.

This architecture has a fundamental privacy problem that no terms-of-service language can fix. When your data leaves your machine, you have lost control of it. You can write policies about data retention. You can encrypt in transit. You can negotiate data processing agreements. But the data still lives on someone else's hardware, processed by someone else's software, subject to someone else's legal jurisdiction.

For consumer applications, this trade-off is widely accepted. For enterprise knowledge work -- where the "data" includes strategic plans, proprietary research, client intellectual property, competitive analysis, and internal communications -- it is a category error. You would not email your client's source code to a stranger for analysis. But that is functionally what happens when you paste it into a cloud-based AI assistant.

The regulatory landscape is tightening. GDPR requires data minimisation and purpose limitation. The EU AI Act imposes obligations on AI systems processing personal data. Sector-specific regulations (HIPAA, FCA, GDPR) restrict where sensitive data can reside. The compliance cost of cloud-based AI is real and growing.

We built Terraphim AI with a different assumption: **your data never leaves your machine.**

## The Architectural Principle: Move Knowledge, Not Data

The core insight that makes local-first AI feasible is that you do not need to send your data anywhere. You need to send the *knowledge extracted from your data* -- and knowledge can be codified, compressed, and moved without exposing the underlying data.

Terraphim's approach has three pillars:

**1. Codify knowledge as graph embeddings, not raw documents.**

Instead of sending documents to a cloud API for processing, Terraphim builds a knowledge graph locally on your machine. Documents are ingested into a `RoleGraph` -- a curated knowledge graph specific to your role. The graph extracts entities, relationships, and ranked relevance. This graph is the portable artefact. It can be shared, versioned, and deployed without ever exposing the source documents.

A CTO's RoleGraph prioritises strategic documents. An engineer's RoleGraph prioritises implementation details. Same underlying data, different knowledge representations.

**2. Index knowledge with deterministic automata, not neural embeddings.**

The retrieval layer uses Aho-Corasick finite state automata compiled from curated taxonomy files. Not BERT embeddings. Not vector databases. Deterministic string matching at 5-10 nanoseconds per pattern.

```rust
let ac = AhoCorasick::builder()
    .match_kind(MatchKind::LeftmostLongest)
    .ascii_case_insensitive(true)
    .build(keys)?;
```

The automaton compiles in ~20 milliseconds when the taxonomy changes. It runs in O(n) on input text length regardless of vocabulary size. It is 5,000 times faster than transformer-based matching. And it is 100% deterministic: same input, same output, every time, on every machine.

This is not a trade-off. For operational AI assistants that retrieve known procedures, deterministic matching is strictly better than probabilistic matching. You do not need fuzzy semantic search to find "deploy procedure for the payment service." You need exact, reproducible, auditable retrieval.

**3. Deploy the knowledge, not the data.**

Because graph embeddings are compact -- a knowledge graph for a specific domain might be a few megabytes, compared to gigabytes of source documents -- they can be deployed anywhere. Including places where raw data cannot go.

The `terraphim_automata` crate compiles to WebAssembly. The knowledge graph runs in a browser tab. It runs at the edge. It runs on a Raspberry Pi. It runs offline, with no network connection, because the retrieval engine has no external dependencies.

This is what "privacy-first" actually means architecturally. Not "we encrypt your data before sending it to the cloud." Not "we have a data processing agreement." It means the system is physically incapable of exfiltrating your data because the data never enters the processing pipeline in the first place.

## The Technology Stack: 58 Crates, Zero Cloud Calls

Terraphim AI is built as a workspace of 58 Rust crates. The key architectural components:

**terraphim_automata** -- Aho-Corasick matching, FST-based autocomplete, fuzzy search. Compiles to WASM. Published as `@terraphim/autocomplete` on npm for browser use, and `terraphim-automata` on PyPI for Python integration.

**terraphim_rolegraph** -- Per-role knowledge graphs with thesaurus management, node/edge ranking, and document indexing. The `RoleGraph` struct holds the complete searchable graph in memory.

**terraphim_persistence** -- Pluggable storage backends. Default configuration uses SQLite (embedded, no server) and in-memory DashMap. Optional backends for Redis, ReDB, and IPFS. No backend requires a running server unless you explicitly configure one.

**terraphim_agent** -- The CLI agent that orchestrates search, learning capture, and session management. Works offline by default. The REPL operates without any network connection.

**terraphim_hooks** -- Knowledge graph-based text replacement that intercepts commands and applies transformations. Runs as a local hook, no cloud round-trips.

**terraphim_rlm** -- Recursive Language Model orchestration for complex multi-step tasks. Supports three execution backends: Local (default on Mac, fully local), Docker (portable isolation), and Firecracker (microVM on server). The local backend requires nothing beyond the binary itself.

The persistence layer is worth emphasising. The default configuration stores everything locally:

```toml
[default]
features = ["sqlite", "dashmap", "memory"]
```

No PostgreSQL. No Redis server. No cloud database. SQLite as the embedded relational store, DashMap for in-memory concurrent access, and an in-memory backend for transient data. The system works out of the box with zero infrastructure.

## Action-Oriented Ontologies: Start With What You Need to Do

A key architectural decision in Terraphim's privacy model is the design of the knowledge graphs themselves. We do not try to model everything. We model what you need to *do*.

This is the action-oriented ontology principle. As I wrote on our Discourse forum when we first articulated the approach: if you think about self-driving cars, the system needs to recognise many objects but only do five things -- go forward, left, right, reverse, and stop. If you start with what you need to do next, the solution search space can be designed very small, resulting in a compact knowledge graph.

Compact knowledge graphs are privacy-enabling. A massive ontology that captures every possible entity and relationship in a domain requires massive data to populate. A compact ontology that captures only the entities and relationships relevant to specific actions requires much less data, and the data it does require is directly tied to purpose.

This is not just a design preference. It is a GDPR compliance strategy. Data minimisation requires that you collect only the data necessary for the specified purpose. An action-oriented ontology makes "necessary" a precise, auditable boundary: you collect exactly the entities and relationships that support the actions your system performs. Nothing more.

## Role-Based Lenses: Privacy at the Individual Level

Different roles see different concept spaces over the same underlying knowledge. This is the role-based lens system.

A project manager working on a client engagement needs access to timeline, budget, and risk information. A developer on the same project needs access to API specifications, code architecture, and deployment procedures. The same project, two completely different knowledge representations.

In a cloud system, role-based access control (RBAC) is implemented by filtering results server-side. The server has access to everything and returns only what the role permits. This means the server holds all data for all roles -- a concentration of access that is itself a privacy risk.

In Terraphim, each role has its own RoleGraph. The CTO graph is a separate artefact from the Engineer graph. They may be derived from overlapping source documents, but the graphs themselves are independent, portable, and can be shared or revoked individually. You can give someone the Engineer graph without giving them the CTO graph, and no server-side filtering is required because the data the CTO sees was never in the Engineer's graph.

This is privacy by design, not privacy by policy.

## When Cloud Is Needed: The Hybrid Pattern

Terraphim is local-first, not local-only. There are legitimate reasons to call cloud APIs: LLM reasoning for novel queries that the local graph cannot answer, model fine-tuning on domain-specific data, collaborative knowledge graph sharing across a team.

The architecture handles this through strict separation of concerns:

- **Retrieval** is always local. The Aho-Corasick automata run on your machine. No query ever leaves your network for retrieval.
- **Reasoning** can be cloud-based. When the local graph returns nothing, the system can escalate to an LLM. But only the *query* goes to the cloud -- not your document corpus, not your knowledge graph, not your taxonomy. And the LLM's response is captured locally, growing the graph so the next occurrence does not need cloud access.
- **Storage** is always local. Persistence uses embedded SQLite by default. Even when you configure remote backends, the data is encrypted and the connection is direct (no Terraphim intermediary server).

The economic property of this hybrid is important: **it gets cheaper as it learns**. The first time you ask a novel question, you pay for LLM reasoning. The thousandth time, the answer comes from the local graph in nanoseconds. Cloud spend decreases over time as the local knowledge grows.

This is the opposite of cloud-native AI, where every query costs the same regardless of how many times you have asked it before. Cloud AI has no memory. Terraphim has persistent, local memory that compounds.

## WASM Deployment: Knowledge Graphs in the Browser

The `terraphim_automata` crate compiles to WebAssembly. The npm package `@terraphim/autocomplete` provides autocomplete, fuzzy search, and knowledge graph queries that run entirely in the browser.

This is not a demo. It is a deployment target. A knowledge graph for a specific domain -- say, a company's internal terminology and procedures -- can be compiled into an automaton, shipped as a WASM module, and queried client-side with zero network requests. The autocomplete in your internal wiki can be powered by a Terraphim automaton that never calls a server.

The same Rust code runs on the server (via the CLI agent), in Docker (via the orchestrator), in Firecracker microVMs (via the ADF), and in the browser (via WASM). Four deployment targets, one codebase, zero data movement.

## The Honest Limitations

Terraphim's approach trades flexibility for privacy. You cannot query arbitrary natural language against an unstructured document corpus without either (a) sending the corpus to a cloud API or (b) building a massive local model. Terraphim does neither. It queries curated, structured knowledge. If the knowledge is not in the graph, the query returns nothing.

This means Terraphim requires curation discipline. Someone has to define the taxonomy, maintain the thesaurus, and ensure the knowledge graph reflects the current state of the domain. This is human work. It cannot be automated away.

The trade-off is deliberate. In enterprise settings -- healthcare, finance, defence, legal -- curation discipline is not optional anyway. Regulatory requirements demand that knowledge representations be auditable, versioned, and attributable. A knowledge graph maintained by domain experts is more compliant than a vector database populated by an opaque embedding model.

## Why This Matters Now

The AI industry is converging on a single architecture: upload your data, pay per token, trust the provider. This architecture is efficient for the provider. It is problematic for anyone whose data has regulatory, competitive, or ethical sensitivity.

Terraphim demonstrates an alternative. A complete AI assistant -- search, learning, orchestration, multi-agent coordination -- that runs on your hardware, stores data in your SQLite database, and only calls external services when you explicitly choose to. The retrieval layer is deterministic and reproducible. The knowledge graphs are portable and auditable. The deployment targets include the browser.

Privacy-first AI is not a feature. It is an architecture. And the architecture either prevents data exfiltration by design, or it does not. There is no middle ground.

Terraphim is open source (MIT/Apache-2.0) at [github.com/terraphim/terraphim-ai](https://github.com/terraphim/terraphim-ai). The core crates -- `terraphim_automata`, `terraphim_rolegraph`, `terraphim_agent` -- are all available on crates.io, npm, and PyPI. Install it. Run it locally. Your data stays on your machine.
