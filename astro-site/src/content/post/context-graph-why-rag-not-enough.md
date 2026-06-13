---
title: "The Context Graph: Why RAG Is Not Enough"
subtitle: "RAG was step one. GraphRAG was step two. The progression leads to context graphs -- where structure itself carries information that LLMs can read."
slug: "context-graph-why-rag-not-enough"
description: "Why Retrieval-Augmented Generation is insufficient for production AI, how GraphRAG and ontologies extend it, and where context graphs fit in the progression from text chunks to structured knowledge."
tags: ["rag", "knowledge-graph", "context-engineering", "ai"]
author: "Dr Alexander Mikhalev"
date: "2026-05-10"
draft: false
---

I have never been fond of the term RAG. And I am not about to say all you need are graphs -- the term GraphRAG has its own problems, especially after Microsoft co-opted it. Context Engineering has always felt like a better fit, but it never seemed to gain traction.

Until perhaps now.

## What Is a Context Graph?

Put simply, a context graph is a triples-representation of data that is optimised for usage with AI. That seems simple enough -- and that is what I thought when I started on the knowledge graph journey years ago as well.

## The Ambiguity Problem: What Is a Knowledge Graph?

Good question. Sit around a table of knowledge graph experts, ask that one, and wait for the arguments to begin. The knowledge graph community is extremely evangelical about what the "right way" is to do things. Imagine discussing politics on Twitter except with obscure references to information theory and linguistics.

The confusion starts immediately: Is a knowledge graph something you store, or is it how you store something? It is not just a knowledge graph -- it is also a graph database. That distinction matters, but the boundaries are blurry.

The word "knowledge" itself is slippery. People have a good grasp of information and data, but what is knowledge? Is it the result of enriching data? Is knowledge when you can take action on data? These questions do not have clean answers.

## It Is Only a Model

Ultimately, a knowledge graph is a data model -- how you organise data. There are many ways to do this at many levels of scale.

### Data in 3 Parts: The Triple

It is all about the triple:

```
Subject -> Predicate -> Object
```

That is it. When people talk about knowledge graphs, they are generally talking about a collection of triples. A triple represents a relationship between two data points:

```
Alice -> isMotherOf -> Bob
```

The term "predicates" comes from predicate logic which has its origins in the 19th century. The use of predicates in the knowledge graph sense appeared in the 1960s with the rise of "semantic networks." The rise of the internet and the dream of the semantic web took predicates to the mainstream.

### The Semantic Web and RDF

RDF (the Resource Description Framework) adds structure to the triple concept by introducing classes, types, ranges, and strict syntax rules. The semantic web aimed to make knowledge representation mainstream by providing a standard framework that anyone could use.

What many find odd about RDF is its use of URIs -- often in the form of URLs. Why use web addresses as identifiers? The vision was interoperability: having globally unique identifiers ensured that two systems using the same URI would be referring to the same entity. Do the URLs themselves matter? No. That is a fair source of confusion.

RDF supports multiple serialisation formats. RDF/XML follows XML structure but is painful for humans. N-Triples is just a list of triples with required URIs. For those who like JSON, there is JSON-LD. The most human-readable format is Turtle.

RDF is incredibly mature and robust. However, learning it independently is nearly impossible -- the very definition of tribal knowledge.

### Property Graphs

Here is where property graphs and RDF fundamentally diverge: Property graphs strictly differentiate between properties (connections to literal values) and relationships (connections to nodes). In RDF, you could use OWL to specify how things relate and RDFS range declarations to define what types of objects are permitted, providing much more flexibility.

Another key difference: property graphs allow properties on edges. You can model something similar in RDF, but edge properties are a simple way of doing something that becomes quite complex in RDF. This is a genuine advantage of the property graph approach.

## The Machine-Readable Insight

While we marvel at the generative capabilities of LLMs, perhaps the biggest disruption is their ability to work with both human-readable and machine-readable data. An LLM can understand text, images, software code, complex schemas, and ontologies.

This is where our experimental work became revealing. We tested various context structures -- CSVs, symbol-based representations, bulleted lists, numbered lists. Surely, with more concise structures, LLM outputs would improve, right?

Wrong. Providing context in structured formats like Cypher or RDF improved responses despite the token overhead. Why? Because the structure itself carries information. When an LLM encounters Cypher or RDF (which it can read fluently), the structure encodes information about what is a node, what is a property, what is a relationship. There is inherent meaning in the syntax itself.

## The Progression: From RAG to Context Graphs

The AI journey follows a clear progression:

1. **LLMs answer questions from their training data** -- sufficient for general knowledge, insufficient for anything specific

2. **RAG appears** -- We stuff prompts with chunks of text to add knowledge, using semantic similarity search over vector embeddings to find the text chunks

3. **GraphRAG emerges** -- Breaking away from text chunks and semantic similarity search alone, we use flexible knowledge representations that can be navigated and refined for better control, capturing rich relationships between entities and concepts

4. **Ontology RAG** -- We take control over what gets loaded into graphs, using structured ontologies for precision and improved recall

This progression is revealing. Step 3 makes minimal use of existing graph algorithms. Step 4 pulls ontologies from the toolbox. We are genuinely scratching the surface of what graph tooling can do.

### What comes next:

5. **Information retrieval analytics tuned to different data types** -- Specialised retrieval strategies for temporal data, accuracy-sensitive data, anomalies, clustering

6. **Self-describing information stores** -- Information systems that carry metadata about their own structure, allowing retrieval algorithms to adapt automatically

7. **Dynamic information retrieval strategies** -- LLMs derive complete retrieval strategies for information types they have never seen before, generalising from learned patterns

8. **Closing the loop for autonomous learning** -- As the system reinests its outputs, annotating the generative data with metadata that adjusts how information is retrieved

## The Temporal Frontier

Temporal relationships are the next frontier for understanding data. The concept of "truth" is often murky. When we observe how data changes over time, we can assess whether information is "fresh" or "stale." Our instinct is to assume newer data is more trustworthy. Yet that is not always the case.

Freshness and recency are not the same as accuracy and precision. Just because data is old and obscure does not mean it is not still valid.

This connects to the [Retrieval Cost Spectrum](/post/retrieval-cost-spectrum-ai-agents/) -- different retrieval strategies have different latency, cost, and accuracy profiles. Context graphs let you choose the right strategy per query, rather than forcing everything through dense vector similarity.

## A New Paradigm for Interoperability

MCP and A2A set out to achieve interoperability. History confirms this has never been simple. LLMs provide a new opportunity: they enable us to work with dynamic ontologies as never before. Previously, ontologies needed to be static so that retrieval algorithms could be built to understand them. LLMs can read and understand ontologies dynamically.

Perhaps LLMs will finally enable the vision of the semantic web, but with slightly different data structures and more flexible implementation patterns.

Context graphs represent the visions that so many information theorists dedicated their lives to pursuing. The opportunity is enormous.

---

*Terraphim AI implements context graphs with deterministic Aho-Corasick automata and role-based knowledge graphs. [Learn more](https://terraphim.ai).*
