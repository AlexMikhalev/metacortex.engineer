---
title: "BERT models with millisecond inference — The Pattern project"
author: "Alex Mikhalev"
date: 2021-08-07T23:21:05.675Z
lastmod: 2021-09-29T18:29:23+01:00

description: ""

subtitle: ""




aliases:
- "/bert-models-with-millisecond-inference-the-pattern-project-409b2880524d"

---

[Newsletter from NVIDIA about the BERT model with 1.2 milliseconds](https://developer.nvidia.com/blog/nvidia-announces-tensorrt-8-slashing-bert-large-inference-down-to-1-millisecond/) on the latest hardware reminded me that I run BERT QA (bert-large-uncased-whole-word-masking-finetuned-squad) in 1.46 ms on a laptop with Intel i7–10875H on RedisAI during RedisLabs RedisConf 2021 hackathon.

### The challenge:

1) BERT QA requires a user input — question, hence it’s not possible to pre-calculate response from the server like in the case of summarization.

2) At the same time NLP based machine learning relies on the tokenisation step — converting common text into numbers before running inference, so the most common pipeline is tokenisation, inference, select a most relevant answer. During my participation in hackathons in 2020, I observed that it’s not trivial to load GPU for 100% for NLP tasks, hence I came up with the process below:

1. Convert and pre-load BERT models on each shard of RedisCluster ([code](https://github.com/applied-knowledge-systems/the-pattern-api/blob/9387a1a9c7c07af108f968cb42bc8a75b587479b/qasearch/export_load_bert.py))
2. Pre-tokenise all potential answers using RedisGears and distribute potential answers on each shard of Redis Cluster using RedisGears(code for [batch](https://github.com/applied-knowledge-systems/the-pattern-api/blob/9387a1a9c7c07af108f968cb42bc8a75b587479b/qasearch/tokeniser_gears_redisai.py) and for [event-based](https://github.com/applied-knowledge-systems/the-pattern-api/blob/9387a1a9c7c07af108f968cb42bc8a75b587479b/qasearch/tokeniser_gears_redisai_register.py) RedisGears function)
3. Amend calling API to direct question query to shard with most likely answers. [Code](https://github.com/applied-knowledge-systems/the-pattern-api/blob/9387a1a9c7c07af108f968cb42bc8a75b587479b/app.py#L238). The call is using graph-based ranking and zrangebyscore to find the most ranked sentences in response to question and then gets relevant hashtag from sentence key
4. Tokenise question. [Code](https://github.com/applied-knowledge-systems/the-pattern-api/blob/9387a1a9c7c07af108f968cb42bc8a75b587479b/qasearch/qa_redisai_gear_map_keymiss_np.py#L51). Tokenisation happening on shard and uses RedisGears and RedisAI integration via `import redisAI`
5. Concatenate user question and pre-tokenised potential answers. [Code](https://github.com/applied-knowledge-systems/the-pattern-api/blob/9387a1a9c7c07af108f968cb42bc8a75b587479b/qasearch/qa_redisai_gear_map_keymiss_np.py#L62)
6. Run inference using RedisAI. [Code](https://github.com/applied-knowledge-systems/the-pattern-api/blob/9387a1a9c7c07af108f968cb42bc8a75b587479b/qasearch/qa_redisai_gear_map_keymiss_np.py#L70) model run in async mode without blocking the main Redis threat, so shard can still serve users
7. Select answer using max score and convert tokens to words. [Code](https://github.com/applied-knowledge-systems/the-pattern-api/blob/9387a1a9c7c07af108f968cb42bc8a75b587479b/qasearch/qa_redisai_gear_map_keymiss_np.py#L75)
8. Cache the answer using Redis — next hit on API with the same question returns the answer in nanoseconds.[Code](https://github.com/applied-knowledge-systems/the-pattern-api/blob/9387a1a9c7c07af108f968cb42bc8a75b587479b/qasearch/qa_redisai_gear_map_keymiss_np.py#L21) this function uses ‘keymiss’ event.

The code is easier to follow than talking about it, mind casting to relevant data types.

Hardware:

1. Clevo laptop with Intel(R) Core(TM) i7–10875H CPU @ 2.30GHz, 64 GB RAM, SSD

Warning: Pre-tokenisation of answers, while being mathematically simple, is really tedious to debug and due to constant changes inside transformers library breaks easily. It was working on 15th May, it needs to be re-validated if you want to use it now.

There are other ways to mitigate inference delay in user experience, for example, I have “Please wait while I retrieve an answer” text to speech, which will cover few seconds.

Other ways to speed up inference — quantise and serve BERT from ONNX.

* * *
Written on August 7, 2021 by Alex Mikhalev.

Originally published on [Medium](https://medium.com/@alexmikhalev/bert-models-with-millisecond-inference-the-pattern-project-409b2880524d)
