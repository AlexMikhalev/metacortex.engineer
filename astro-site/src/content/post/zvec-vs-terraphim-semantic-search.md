---
title: "zvec vs Terraphim: Two Paths to Semantic Search"
subtitle: "Alibaba's neural vector database versus deterministic knowledge graphs. One scales to billions. The other explains why it matched."
slug: "zvec-vs-terraphim-semantic-search"
description: "A deep dive comparing Alibaba's zvec neural vector database with Terraphim's graph-based approach to semantic search -- when to use which, and why hybrid retrieval is the future."
tags: ["vector-search", "knowledge-graph", "semantic-search", "comparison"]
author: "Dr Alexander Mikhalev"
date: "2026-05-12"
draft: false
---

When it comes to semantic search, there are fundamentally different architectural approaches. Alibaba's zvec and Terraphim represent two distinct philosophies: neural embeddings vs knowledge graphs, scale vs interpretability, dense vectors vs co-occurrence relationships.

## The Core Philosophy

### zvec: Neural Embeddings at Scale

zvec is a lightweight, in-process vector database built on Alibaba's battle-tested Proxima engine. It transforms documents into high-dimensional vectors using neural embedding models (BERT, OpenAI, etc.), then uses Approximate Nearest Neighbor (ANN) algorithms like HNSW to find similar documents.

Key characteristics:

- Dense vectors (typically 384-1536 dimensions)
- ANN indexing (HNSW, IVF, Flat)
- Built-in embedding models (OpenAI, Qwen, SentenceTransformers)
- Billions of vectors, millisecond query times
- Black-box interpretability

### Terraphim: Knowledge Graphs for Understanding

Terraphim takes a radically different approach. Instead of converting documents to opaque vectors, it builds a knowledge graph from term co-occurrences. Each concept becomes a node, relationships become edges, and relevance is calculated by traversing this graph structure.

Key characteristics:

- Co-occurrence graph embeddings
- Aho-Corasick automata for fast pattern matching
- Domain-specific thesauri for synonym expansion
- Role-based graphs for persona-driven search
- Fully explainable relevance scoring

## Architectural Comparison

```
zvec:
  Document -> Neural Encoder -> Dense Vector -> HNSW Index
  Query -> Neural Encoder -> Query Vector -> ANN Search -> Top-K

Terraphim:
  Document -> Term Extraction -> Co-occurrence -> Graph
  Query -> Aho-Corasick Match -> Graph Traversal -> Ranked Docs
```

### Data Structures

| Component | zvec | Terraphim |
|-----------|------|-----------|
| **Storage Unit** | Collection (table-like) | RoleGraph (knowledge graph) |
| **Representations** | Dense/Sparse vectors (768-dim+) | Nodes, Edges, Thesaurus |
| **Index Types** | HNSW, IVF, Flat, Inverted | Hash maps + Aho-Corasick |
| **Persistence** | Disk-based collections | JSON serialisation |

## Feature Matrix

| Feature | zvec | Terraphim |
|---------|------|-----------|
| **Dense Embeddings** | Yes, native | Not used |
| **Sparse Vectors** | Yes, BM25 supported | Yes, BM25/BM25F/BM25Plus |
| **Knowledge Graph** | No | Yes, core architecture |
| **ANN Search** | Yes, HNSW/IVF/Flat | Not applicable |
| **Explainability** | Low (black box) | High (shows graph path) |
| **Synonym Expansion** | Via embedding model | Via explicit thesaurus |
| **Role/Persona Support** | No | Yes, RoleGraphs |
| **Multi-Haystack** | Single collection | Multiple sources |
| **Quantization** | INT8/FP16 | Not needed |

## Performance Characteristics

### zvec (Benchmarks from 10M vector dataset)

- **Throughput**: 2,000-8,000 QPS depending on configuration
- **Recall**: 96-97% with HNSW
- **Latency**: Milliseconds for 10M vectors
- **Scale**: Billions of vectors

### Terraphim (Observed Performance)

- **Throughput**: In-memory graph traversal (very fast)
- **Recall**: Deterministic graph-based ranking
- **Latency**: Sub-millisecond for typical graphs
- **Scale**: Thousands to tens of thousands of documents

This complements the comparison in [GPU KGs vs Deterministic Automata](/post/gpu-kg-vs-deterministic-automata/) -- that post covers NVIDIA RAPIDS and GPU acceleration. This covers zvec specifically, and the fundamental tradeoff between neural embeddings and graph-based search.

## When to Use Which

### Choose zvec When:

1. **You need to search billions of documents** -- ANN algorithms scale to massive datasets
2. **You are building RAG systems with LLMs** -- Dense embeddings align with LLM representations
3. **You need image/audio similarity search** -- Requires dense embeddings, CLIP-style multimodal
4. **Exact semantic similarity matters** -- "King - Man + Woman = Queen" works with dense vectors

### Choose Terraphim When:

1. **You need explainable results** -- "Why did this document rank high?" Graph path shows: matched node X via edge Y to document Z
2. **You have domain-specific knowledge** -- Custom thesauri for technical terms
3. **You are building personal knowledge management** -- Note-taking apps, research assistants
4. **You need role-based search** -- Different personas see different results

## Code Comparison

### Document Indexing

**zvec (Python):**
```python
import zvec

schema = zvec.CollectionSchema(
    name="docs",
    vectors=zvec.VectorSchema("emb", zvec.DataType.VECTOR_FP32, 768),
)

collection = zvec.create_and_open(path="./data", schema=schema)

collection.insert([
    zvec.Doc(
        id="doc1",
        vectors={"emb": embedding_model.encode("Rust async programming")},
        fields={"title": "Async in Rust"}
    ),
])
```

**Terraphim (Rust):**
```rust
use terraphim_rolegraph::RoleGraph;
use terraphim_types::{Document, RoleName};

let mut graph = RoleGraph::new(
    RoleName::new("engineer"),
    thesaurus
).await?;

graph.index_documents(vec![
    Document {
        id: "doc1".into(),
        title: "Async in Rust".into(),
        body: "Rust's async/await syntax...".into(),
        ..Default::default()
    },
]).await?;
```

### Searching

**zvec:**
```python
query_vec = embedding_model.encode("how to write async code")
results = collection.query(
    zvec.VectorQuery("emb", vector=query_vec),
    topk=5
)
# Results ranked by cosine similarity
```

**Terraphim:**
```rust
let results = graph.query_graph("async code", None, Some(5))?;
// Results ranked by:
// 1. Node rank (concept frequency)
// 2. Edge rank (relationship strength)
// 3. Document rank (occurrence count)
```

## Can They Work Together?

The most interesting possibility is hybrid retrieval:

1. **zvec for initial broad retrieval** -- Cast a wide net across millions of documents
2. **Terraphim for reranking** -- Apply domain-specific knowledge graph to refine results
3. **Terraphim for explainability** -- Show *why* a vector-similar document actually connects

```
User: "Why did this document match?"
System:
  - zvec: "Vector similarity: 0.92"
  - Terraphim: "Matched via concepts: async -> tokio -> concurrency"
```

## Conclusion

zvec and Terraphim solve semantic search with fundamentally different approaches:

- **zvec** scales neural embeddings to billions of documents using ANN algorithms. It is the right choice for large-scale RAG systems, e-commerce search, and any application requiring dense vector similarity.

- **Terraphim** builds interpretable knowledge graphs from term relationships. It excels at personal knowledge management, domain-specific expert systems, and any application where understanding *why* a document matched is as important as finding it.

The exciting possibility is combining both: zvec's scale with Terraphim's explainability. The future of semantic search might just be hybrid.
