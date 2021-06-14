---
title: "Old school use of Redis for Data Science and RedisGears"
author: "Alex Mikhalev"
date: 2020-05-16T07:31:33.791Z
lastmod: 2021-06-11T09:59:40+01:00

description: ""

subtitle: ""




aliases:
- "/old-school-use-of-redis-for-data-science-and-redisgears-a5c965eddaca"

---

Since learning that I could not use RedisBloom (also RedisSearch and RedisGraph) on the open-source cluster, I replaced the use of Bloom/Cockoo filter with set — (SADD, SMEMBERS), supported since Redis version 1.

It’s nothing to be writing about, except on thing: the use of Redis cluster changed the dynamic of Data Science project. Normally you build pipeline/parser, you run it, you wait for a bit then you find out your results, you swear a bit and you write a bit of code and then you wait and cycle repeats. I know Redis is fast because I used it in production, but Redis Cluster is also fast. Surprisingly fast.

Re-parsing whole CORD19 dataset — because I decided I don’t want to capture paragraphs and I want to change the key structure for the article — took 7 minutes. Parsing titles from JSON files — I remembered humans don’t like to be presented with SHA256 key of the article in UI, they like titles more ;) and I also remembered that print is blocking operation and added proper logger — took only 3 minutes. Redis Cluster acts as one large high-performance machine despite CPU on my “dedicated server” Intel(R) Core(TM) i7–2600 CPU @ 3.40GH (upgrade the kernel on Ubuntu 18.04 LTS and it would not boot — Chipset is no longer supported).

So I have to **keep cutting the code** instead of waiting for hardware to process calculation. In the past, I spend hours/days in Kaggle challenge learning and debugging memory management problems with dask.distributed, joblib and Neo4j.

I lost data multiple times and at the end of the challenge when I wasn’t sure if Neo4j intake is halfway through dataset I wrote “faster way to populate neo4j”: map entities (nodes) relationship (articles) into Redis keys and export vis redis-cli: `redis-cli --scan --pattern nodes:* |awk '{print "hmget " $0 " id name"}' |redis-cli --csv > nodes.csv` and `redis-cli --scan --pattern edges:* |\ awk '{print "hmget " $0 " source_entity_id destination_entity_id sentence_key"}' |\ redis-cli --csv > edges.csv`

and kicked myself mentally for not using Redis earlier. My Redis instance crashed on consuming 32 GB Ram and it became my submission data, hence now I put effort into rolling out cluster — I know I will need all of it and so far it scales and performs amazingly.

Redis now have a module which I haven’t used in the past and is open source cluster-aware: Redis Gears.

Watch “Event-Driven_Write Behind Redis - Intro to Redis Gears” video from Elena Kolevska if you haven’t done so.

Redis Gears allows you to run Python code directly on the cluster. It’s cluster-aware and supports distributed calculations. But to run python code you need libraries and most of the time, not the once vendor thought about.

But RedisLabs took care of it meet [Redis Gears cli](https://github.com/RedisGears/gears-cli): the tool allows you to submit python code to Redis instance or cluster and pass requirements file. Luckily I deployed RedisCLuster with Gears enabled and don’t need to add it to configuration. I am very tempted to deploy spacy and BERT based tokenisation (maybe via RedisAI? on the second iteration) but as the next incremental step, I would like to add language detection. Reason for it that some of the articles in the corpus were in a different language: I spotted Russian, Chinese, Korean in the search results and obviously if you processed them as English it’s a waste of time. So this time I want to filter them out early.

I am going to use spacy later but there is a simple langdetect module:

```
pip install langdetect
```

and works as

```
from langdetect import detect
# Specifying the language for

# detection

print(detect("Geeksforgeeks is a computer science portal for geeks"))

print(detect("Geeksforgeeks es un portal informático para geeks"))

print(detect("Geeksforgeeks - это компьютерный портал для гиков"))
```

see [write up](https://www.geeksforgeeks.org/detect-an-unknown-language-using-python/). Now turning it into Gears script is as easy as:

```
from langdetect import detect 
  

def detect_language(x):
    #detect language of the article
    if x['value']!='':
        lang=detect(x['value'])
    else:
        lang="empty"
    execute('SET', 'lang_article:' + x['key'], lang)
    if lang!='en':
        execute('SADD','titles_to_delete', x['key'])

gb = GB()
gb.foreach(detect_language)
gb.run('title:*')
```

Now create a requirements file for gears:

```
langdetect==1.0.8
```

And validate deployment:

```
gears-cli --host 127.0.0.1 lang_detect_gears.py --requirements requirements_gears.txt
```

The script above only checks language in the title creates key-value for article language creates a set of articles marked for deletion. Same will be applied to paragraphs (title can be in English but text in a different language) and I will handle deletion separately.

* * *
Written on May 16, 2020 by Alex Mikhalev.

Originally published on [Medium](https://medium.com/@alexmikhalev/old-school-use-of-redis-for-data-science-and-redisgears-a5c965eddaca)
