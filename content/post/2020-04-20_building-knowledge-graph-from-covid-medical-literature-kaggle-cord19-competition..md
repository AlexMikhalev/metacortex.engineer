---
title: "Building Knowledge graph from Covid Medical Literature Kaggle CORD19 competition."
author: "Alex Mikhalev"
date: 2020-04-20T19:25:51.091Z
lastmod: 2021-06-11T09:59:25+01:00

description: ""

subtitle: ""




aliases:
- "/building-knowledge-graph-from-covid-medical-literature-kaggle-cord19-competition-f0178d2a19bd"

---

Using a lack of commute to the office (10 minutes by car or 40 minutes pleasant walk) as my excuse to my family I spent every available minute outside of my working hours to hack the code for the data science competition [Cord19](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge).

Competition stroke too many of my chords to let it go, because I have strong beliefs about search and knowledge management:

- Search or rather information exploration should be spacial, accompanied by text, preferably in VR (memory palace see [Theatre of Giulio Camillo](https://magazine.art21.org/2012/08/30/the-museum-as-memory-palace/#.Xp3BR8hKg2w) ) and the connected graph is a path towards it, assisted by text — relevant text pop up on the connection, where people explore the concepts and then dig deeper into text. Icons enforced on a flat screen is dated concept — it was novel in 1972, time to move on to new technologies.
- When I am exploring topics on science or engineering, I look at the diversity of the opinion, not the variety of the same cluster of words, same opinion. I would like to avoid confirmation bias. Obviously, modern search-related technology is working towards confirmation bias for a variety of reasons.
- I learned Natural Language processing/search engines in the last century, I am trying to keep up with current SOTA and liked to stretch that muscle, particularly on such interesting dataset.

### Approach

My approach was more engineering than Data Science one: I wanted to extract “knowledge” from a bunch of unstructured documents (which were not spell checked) and build a knowledge graph by mapping the entities from the articles into industry-standard ontology (Universal Medical System)

### Step 1

1) parse paragraphs into sentences (using spacy)

2) sentences into tokens and expand abbreviations (using scispacy)

3) map tokens into entities (using scispacy)

4) map entities into external ontology — Universal Medical System terms aliases (as synonyms) using UmlsEntityLinker from scispacy. Code is on [Step1 notebook](https://www.kaggle.com/alexmikhalev/step-1ingesttosqlitedatabase) Output of Step 1 available on public google cloud platform bucket.

`Project id=cord19kaggle bucket=kagglecord19largemodel` filename `entities_synonims_table_large_model.zip and sentences_table_large_model.zip` - Postgres `COPY` command

The first lesson learned: you need decent hardware to participate: most of the modern approaches assume batch processing mode and GPU alignment. My raspberry pi 4 wasn’t enough, so I ended up using NC6 instance in Azure and Macbook Pro. Ended up rolling out the PostgresSQL server at Hetzner dedicated server to make sure interim computations are saved. I wanted to re-use scispacy and scispacy in-memory models (9 GB RAM just on import), but parallelize file read and processing. After spending time with dask dataframe and joblib I found out both of them serialize in-memory objects on disk before loading inside of the process (kind of what you would expect). This is where it broke — it didn’t like the internal scispacy model and crashed consistently. What is the easiest serializable entity, which is commonly used to store and process larger than memory ? Database connection and database. I choose PostgreSQL — in the past, my team in Shopitize manage to cook it to ms response time.

Lessons learned 2: Even in the database, ~50000 articles is a large volume. My MacBook died, then I maxed out storage on Azure NC6 GPU instance, had to go to ephemeral one, downside — I lost data more than once and what is more important time, pre-processing articles on Azure instance took roughly a week.

Lessons learned 3: Mess with docker: having own infrastructure also important to make sure you docker+cuda driver + libraries match. I had a script from a few years back to bootstrap azure with Nvidia docker. I spend the half-day trying to get it all working: Kaggle docker assumes ubuntu 16.04, while NVidia data science workbench is on 18.04. Depending on your luck milage vary. Ended up using Azure instance with the default Microsoft data science template.

Leassons learned 5: Doing it with kids at home results in hilarious copy-paste errors —` %%timeit -r5` instead of `%%time` in notebook cell which runs for 20 hours. Genius.

Stupid mistake number 2: calling fetch on PG output. Run out of memory and disk space while fetching 90 GB of text.

### Step 2

5) Build Aho-Corasic automata from stored entities and synonyms, the key is concept id from UMLS above. Output available on [http://kaggle.com/cord19acautomatalargemodel](http://kaggle.com/cord19acautomatalargemodel)

Code is [Step2 notebook](https://www.kaggle.com/alexmikhalev/step2build-automata-from-pgentities-to-synonyms)

Lessons learned: I love automata, they are superb, hilariously quick. Aho Corasick has been around for years you can use it as an interview question. Downside they are a single thread. Any attempt to parallelize will result in some strange construct. So what? Just read 50000 articles via SQL select takes time. Like 9 hours.

### Step 3

6) build a relationship (pairs of terms ) from sentences by matching into Automata into sentences and save to Knowledge Graph Database as edges. (Neo4j) [Step3 Notebook](https://www.kaggle.com/alexmikhalev/step3-matchentitiestoneo4j)

6.1) faster option proved to be map entities (nodes) relationship (articles) into redis keys and export vis redis-cli

I created a dump of redis cache to “handcraft” knowledge graph using (from step 6.1 above): `redis-cli --scan --pattern nodes:* |awk '{print "hmget " $0 " id name"}' |redis-cli --csv > nodes.csv` and `redis-cli --scan --pattern edges:* |\ awk '{print "hmget " $0 " source_entity_id destination_entity_id sentence_key"}' |\ redis-cli --csv > edges.csv` This is a partial dump of the dataset (about 347800 sentences) Output available on [SampleCord19](https://www.kaggle.com/alexmikhalev/samplecord19knowledgegraph)

### Create a knowledge graph in Neo4J

7) create a nodes CSV for nodes

8) create a edges csv for relationship

9) Use nodes-admin import nodes and edges

Neo4J allows a large number of tools for visualization, querying and building transformation, screenshots and code examples below, but to demonstrate submission I “handcraft”ed graph database and visualization.

### Justification

I wanted to map entities to an existing body of medical knowledge — initially external, but this can evolve into creating a localized knowledge base specific to coronavirus/SARS. Using databases — graph or SQL will allow reviewing matched terms re-process synonyms and build improvement cycle plugging a new dictionary starting from step 1.3.

### Further work

- Provide relevance metric to output — currently randomly selected 10 articles/keys for each question
- Rewrite parts of pipeline in Rust and use Redis more

I had high hopes for Neo4j in the beginning, the downside was I didn’t manage to complete step3 with Neo4j — it took over a few days and resorted to Redis and then handcraft visualization and graph structure for submission. What surprised me how good Redis performance was and I regret not to start using it earlier. For the next round, I will build pipeline around Redis and RedisGraph.

### Conclusion

Pipeline works as I want it, now is a time to re-iterate and improve, whether competition or not I intend to turn it into an open-source project. Stay tuned for source code in github, major lessons learned: Kaggle competition is a project (endeavor) with all associated activities — planning towards the deadline, assembling and enabling team, enabling capabilities — hardware and office space/hours.

* * *
Written on April 20, 2020 by Alex Mikhalev.

Originally published on [Medium](https://medium.com/@alexmikhalev/building-knowledge-graph-from-covid-medical-literature-kaggle-cord19-competition-f0178d2a19bd)
