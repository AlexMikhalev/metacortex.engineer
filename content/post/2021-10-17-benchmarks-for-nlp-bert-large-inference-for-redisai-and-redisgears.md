---
title: "Benchmarks for BERT Large Question Answering inference for RedisAI and RedisGears"
slug: benchmarks-for-nlp-bert-large-inference-for-redisai-and-redisgears
description: 
tags: redis,redis-cluster,redisai,redisgears,benchmark
author: Alex Mikhalev
username: alexmikhalev
date: 2021-10-17
---

# Benchmarks for BERT Large Question Answering inference for RedisAI and RedisGears


pre-requisite for running the benchmark:

Assuming you are running Debian or ubuntu, have docker and docker-compose (or can create virtual environment via conda):

```
git clone -b benchmark — recurse-submodules git@github.com:applied-knowledge-systems/the-pattern.git
```

```
cd the-pattern
```

```
./bootstrap_benchmark.sh
```

It should end with curl call to qasearch API, redis caching is disabled for benchmark, it’s a small cluster – 8 nodes in total (fixed in config.sh)

Curl call shall look like this:

```
curl -i -H “Content-Type: application/json” -X POST -d ‘{“search”:”Who performs viral transmission among adults?”}’ http://localhost:8080/qasearch
```

```
HTTP/1.1 200 OK
```

```
Server: gunicorn
```

```
Date: Fri, 15 Oct 2021 22:11:23 GMT
```

```
Connection: close
```

```
Content-Type: application/json
```

```
Content-Length: 426
```

```
{“links”:[{“created_at”:”2001",”rank”:29,”source”:”C0001486",”target”:”C0152083"}],”results”:[{“answer”:””,”sentence”:”Initially the 5 most gene 1 of the viral genome is translated into the viral A dROp which then replicates the viral genomic ANAs into negative strand ANAs”,”sentencekey”:”sentence:PMC302072.xml:{8YG}:11",”title”:”Heterogeneous nuclear ribonucleoprotein A1 regulates RNA synthesis of a cytoplasmic virus”}]}
```

There is a sentence key with shard id or grab “Cache key” from docker logs -f rgcluster, one more thing is to figure out from logs the port of the shard corresponding to hashtag (also known as shard id, stuff in curly brackets – like this {8YG}, same will be in the output for export_load script.

Check that call works:

```
redis-cli -c -p 30003 -h 127.0.0.1 get “bertqa{8YG}_PMC302072.xml:{8YG}:10_Who performs viral transmission among adults”
```

and then run the benchmark

```
redis-benchmark -p 30004 -h 127.0.0.1 -n 10 get “bertqa{356}_PMC126080.xml:{356}:1_Who performs viral transmission among adults”
```

-n = number of times.

add

– csv if you want to output in CSV format

– precision 3 – if you want more decimals in ms

More information about benchmarking tool https://redis.io/topics/benchmarks

if you don’t have redis-utils installed locally, you can run the same via

```
docker exec -it rgcluster /bin/sh -c “redis-benchmark -r 10000 -n 10000 PING”
```

The platform only has 20 articles, 8 Redis nodes = 4 masters + 4 slaves, so relevance would be bad and doesn’t need a lot of memory.

There are many ways to optimise this deployment for example add FP16 quantization and ONNX runtime, this [script](https://github.com/applied-knowledge-systems/the-pattern-api/blob/7bcf021e537dc8d453036730f0a993dd52e1781f/qasearch/export_load_bert.py) will be a good starting point.
