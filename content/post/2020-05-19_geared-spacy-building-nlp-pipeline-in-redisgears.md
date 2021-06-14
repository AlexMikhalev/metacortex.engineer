---
title: "Geared Spacy: Building NLP pipeline in RedisGears"
author: "Alex Mikhalev"
date: 2020-05-19T08:25:25.856Z
lastmod: 2021-06-11T09:59:45+01:00

description: ""

subtitle: ""

images:
 - "/post/img/2020-05-19_geared-spacy-building-nlp-pipeline-in-redisgears_0.png"


aliases:
- "/geared-spacy-building-nlp-pipeline-in-redisgears-c14f7a52652d"

---

Initially, I only planned to use Redis Cluster as one large in-memory store/database, store all article ids in the set corresponding to the pipeline step and then run: for each article_id in a set, apply next step in the pipeline, save id into next set. Potentially explore nomad to distribute compute.

Next few steps are memory demanding and I mean it, but the temptation to use RedisGears to distribute calculation over Redis Cluster with no effort on my side was too great. I even didn’t finish watching [Tutorial](https://www.youtube.com/watch?time_continue=1&v=Dzf9nIkPwX0&feature=emb_title), when I started coding (hint: watch the tutorial first). Inspired by the quick success of [language detection](https://medium.com/@alex.mikhalev/old-school-use-of-redis-for-data-science-and-redisgears-a5c965eddaca) I decided to add spacy and small English model into dependencies:

```
langdetect==1.0.8
spacy
https://github.com/explosion/spacy-models/releases/download/en_core_web_md-2.2.5/en_core_web_md-2.2.5.tar.gz
```

Doesn’t look much — spacy is 10MB download and smallest English model 90 Mb.

The picture is different if you import both:

![](/post/img/2020-05-19_geared-spacy-building-nlp-pipeline-in-redisgears_0.png#layoutTextWidth)

Spacy consumes(reserves) 1GB RAM just on import model (small one), above is a plot of simplest spacy test:

```
import spacy

nlp=spacy.load('en_core_web_md')
```

it will only raise to 1.2 GB if I start processing (with one item). At this stage in NLP pipeline, I only need to turn paragraphs into sentences and I want to use only Dependency Parser from spacy, so I will disable the rest:

nlp=spacy.load(‘en_core_web_md’, disable=[‘ner’,’tagger’])

Memory consumption didn’t change — it’s still 1.2 GB RAM for processing paragraphs, the question will RedisGears cope?

Redis trivia: do you know how large Redis source code and binary?

It coped surprisingly well:

```
import spacy 
nlp=spacy.load('en_core_web_md', disable=['ner','tagger'])
nlp.max_length=2000000

def remove_prefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix):]

def parse_paragraphs(x):
    key_prefix="paragraphs:"
    #make sure we only process english article
    lang=execute('GET', 'lang_article:' + x['key'])
    if lang=='en':
        paragraphs =x['value']
        doc=nlp(paragraphs)
        idx=1
        article_id=remove_prefix(x['key'],key_prefix)
        for each_sent in doc.sents:
            sentence_key=f"sentences:{article_id}:{idx}"
            execute('SET', sentence_key, each_sent)
            idx+=1
        execute('SADD','processed_docs_stage2_sentence', article_id)
    else:
        execute('SADD','screw_ups', x['key'])
    

gb = GB()
gb.foreach(parse_paragraphs)
gb.count()
gb.run('paragraphs:*')
```

The simple script above submitted via redis-cli into cluster

```
SECONDS=0

gears-cli --host 10.144.83.129 --port 6379 spacy_sentences_geared.py --requirements requirements_gears_spacy.txt

echo "spacy_sentences_geared.py finished in $SECONDS seconds."
```

The original version didn’t have `gb.count` in it and was returning all processed records back to the client (all 11 GB), this is where I was running out of patience and/or bandwidth. Thanks to [**meirsh**](https://forum.redislabs.com/u/meirsh)and[RedisLabs forums](http://forum.redislabs.com/c/modules/redisgears) time processing time was reduced down to a reasonable 30 minutes.

Next step is also memory hungry — tokenisation and Gavin D’mello had a crack on it, but discussion on forums sparked some thoughts: I was coming with data science hat on — we have a data frame in, it’s all batch. But if you think about the NLP pipeline, only the first step — intake is batch. The rest of the pipeline doesn’t really care whether it’s batch or event-driven, steps would be the same and I can leverage more of the good code and work of RedisLabs team inside RedisGears, back to drawing boards.

* * *
Written on May 19, 2020 by Alex Mikhalev.

Originally published on [Medium](https://medium.com/@alexmikhalev/geared-spacy-building-nlp-pipeline-in-redisgears-c14f7a52652d)
