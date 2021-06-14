---
title: "Processing COVID-19 literature: intake into Redis Cluster and Cbloom filter"
author: "Alex Mikhalev"
date: 2020-05-14T08:11:10.078Z
lastmod: 2021-06-11T09:59:38+01:00

description: ""

subtitle: ""




aliases:
- "/processing-covid-19-literature-intake-into-redis-cluster-and-cbloom-filter-e387af01c691"

---

In the last article, I span up Redis Cluster. This time is to populate it with data. This time I am not going to create a one large data science pipeline, which takes 9 GB RAM just to start, but I am going to split it into “nano” services, which I can debug easily (and hopefully add tests :) at some point.

Kaggle CORD19 data is one sizeable zipped archive with a bunch of JSON files, download Kaggle dataset and unzip.

```
$ kaggle datasets download allen-institute-for-ai/CORD-19-research-challenge
$ unzip CORD-19-research-challenge.zip
```

Just a small intake script:

[AlexMikhalev/cord19redisknowledgegraph](https://github.com/AlexMikhalev/cord19redisknowledgegraph/blob/master/RedisIntakeCbloomRedisCluster.py "https://github.com/AlexMikhalev/cord19redisknowledgegraph/blob/master/RedisIntakeCbloomRedisCluster.py")

Take all:

- json_files-> parse_json: parse article_id
- parse `body_text` return all text as paragraphs
- Store paragraphs in Redis with article_id:paragraph_id

JSON can be parsed really fast, the role of RedisBloom (Cockoo) filter is to prevent re-processing of files on each step and I was planning to use different filters for each stage. When processing JSON to Redis — I may not care that much, but if I am processing text via BERT/Transformers it will take some time per each line/file.

Unfortunately, RedisBloom python library doesn’t support Redis cluster, so I will have to roll back to storing set in Redis. If I am going to redo this intake for single machine configuration I will re-do it with Rust and [Xor-filter](https://github.com/bnclabs/xorfilter).

For now, I stored the Cockoo filter in local Redis instance while populating Redis-Cluster. Good news script run on my laptop (Windows 10) 8 GB RAM. Successfully.

* * *
Written on May 14, 2020 by Alex Mikhalev.

Originally published on [Medium](https://medium.com/@alexmikhalev/processing-covid-19-literature-intake-into-redis-cluster-and-cbloom-filter-e387af01c691)
