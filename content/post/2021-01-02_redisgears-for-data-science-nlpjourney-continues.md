---
title: "RedisGears for Data Science NLP — Journey continues"
author: "Alex Mikhalev"
date: 2021-01-02T00:13:29.733Z
lastmod: 2021-06-11T10:00:08+01:00

description: ""

subtitle: ""




aliases:
- "/redisgears-for-data-science-nlp-journey-continues-1ae19265526"

---

If you procrastinate on the open-sourcing project for several months, you forget what you wanted to do before. I thought I wanted to split into streams-based code and open source it, then after completing most of the work I realised I wanted to build an open-source project based on KeysReader part of [cord19project](https://github.com/AlexMikhalev/cord19redisknowledgegraph)— it’s way easier to debug and fits better into DataScience flow: create a batch script, run, validate, register for new data by changing [GearsBuilder.run](http://gearsbuilder.run) to register.

Also looking at my own code now — it’s not something to be proud of or put into production.

So, let’s rewrite it.

1. I want to be able to run it at the laptop (although 256 GB RAM server on standby for demo)
2. It should not be that ugly. It’s a hobby data science project, so few things here and there are ok, but it shall be readable (and hopefully contributable)
3. Do I care about taking snapshots on every step? No, I only want “interim” — when sentences are spellchecked, so I can hook BERT based tokeniser as a subscriber.

How can I fit NLP pipeline into RedisGears better?

1. For each record — detect language (discard non English), it’s [“filter”](https://oss.redislabs.com/redisgears/operations.html#filter)
2. Map paragraphs into a sentence — [flatmap](https://oss.redislabs.com/redisgears/operations.html#flatmap)
3. Sentences spellchecker — it’s [“map”](https://oss.redislabs.com/redisgears/operations.html#map)
4. Save sentences into hash — [processor](https://oss.redislabs.com/redisgears/operations.html#processor)

And since there is no support for multiple files in a RedisGears project there is no point of splitting project into that many files. Let’s consolidate it into smaller chunks.

New branch pushed into [github](https://github.com/applied-knowledge-systems/the-pattern-platform/).

* * *
Written on January 2, 2021 by Alex Mikhalev.

Originally published on [Medium](https://medium.com/@alexmikhalev/redisgears-for-data-science-nlp-journey-continues-1ae19265526)
