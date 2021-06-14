---
title: "CORD19 competition project into Open Source project"
author: "Alex Mikhalev"
date: 2020-12-28T15:29:44.145Z
lastmod: 2021-06-11T10:00:06+01:00

description: ""

subtitle: ""




aliases:
- "/cord19-competition-project-into-open-source-project-87fbd0d261e1"

---

I was planning to turn my RedisHack/Kaggle [competition project](https://github.com/AlexMikhalev/cord19redisknowledgegraph) into set of smaller open source projects for several months now.

Here is the first one: RedisGears based NLP pipeline [https://github.com/applied-knowledge-systems/the-pattern-platform](https://github.com/applied-knowledge-systems/the-pattern-platform) — turn text into knowledge graph (stored in RedisGraph) using Medical Ontology (methathesaurus). Why Redis (Gears)? This pipeline takes about 6 hours to process 50K articles with peak 80 GB RAM. It takes about a week to process the same 50K articles using python’s scispacy (and land into Neo4j). UI, API, BERT QA and BERT Summary deployments will follow.

This is my attempt to turn the competition project into something which will hopefully be useful to others. Leave comment, PR or Issue to help me to continue working on it.

* * *
Written on December 28, 2020 by Alex Mikhalev.

Originally published on [Medium](https://medium.com/@alexmikhalev/cord19-competition-project-into-open-source-project-87fbd0d261e1)
