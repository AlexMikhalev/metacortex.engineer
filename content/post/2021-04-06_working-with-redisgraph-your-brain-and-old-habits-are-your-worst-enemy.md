---
title: "Working with RedisGraph: your brain and old habits are your worst enemy"
author: "Alex Mikhalev"
date: 2021-04-06T10:16:04.027Z
lastmod: 2021-06-11T10:00:20+01:00

description: ""

subtitle: ""




aliases:
- "/working-with-redisgraph-your-brain-and-old-habits-are-your-worst-enemy-88e57c38831a"

---

One of the things I noticed in my hobby project working with Redis I started overthinking and over optimising:

Consider old code [here](https://github.com/AlexMikhalev/cord19redisknowledgegraph/blob/master/graphsearch/graph_search.py) — it makes two calls to RedisGraph, one to fetch edges and then another one to turn node ids to list of dictionary `{id:node_id,name:node_name}`, both queries are trivial:

```
#fetch edges
WITH $ids as ids    MATCH (e:entity)-[r]->(t:entity) where e.id in ids RETURN DISTINCT e.id,t.id,max(r.rank) ORDER BY r.rank
#fetch nodes
WITH $ids as ids     MATCH (e:entity) where e.id in ids RETURN DISTINCT e.id,e.name,max(e.rank)
```

But when I added years to nodes properties I decided to “optimise” and fetch node names in the same query, this is probably what you would normally do for SQL server:

```
WITH $ids as ids MATCH (e:entity)-[r]->(t:entity) where (e.id in ids) and (r.year in $years) RETURN DISTINCT e.id, e.name,e.rank, t.id, t.name, t.rank, max(r.rank), r.year ORDER BY r.rank DESC
```

Full code [here](https://github.com/applied-knowledge-systems/the-pattern-api/blob/12c2a1e79b93a48366cb02dfa4e4bfd5b08a7cf5/graphsearch/graph_search.py). But then now I need to traverse via RedisGraph output to shape dict, and then flatten dict in python so I can serialize it to JSON and return to three.js.

```
#flatten dict
node_list=[{'name':k,'id':node_dict[k]['id'],'rank':node_dict[k]['rank']} for k in node_dict]
```

Hold on a second, all this python code to save on query which takes between 30 to 100 milliseconds response?

Now I am putting back the old code.

* * *
Written on April 6, 2021 by Alex Mikhalev.

Originally published on [Medium](https://medium.com/@alexmikhalev/working-with-redisgraph-your-brain-and-old-habits-are-your-worst-enemy-88e57c38831a)
