---
title: "Lessons learned for CORD19: Deploying your computation infrastructure"
author: "Alex Mikhalev"
date: 2020-04-30T20:25:10.521Z
lastmod: 2021-06-11T09:59:28+01:00

description: ""

subtitle: ""

images:
 - "/post/img/2020-04-30_lessons-learned-for-cord19-deploying-your-computation-infrastructure_0.png"

aliases:
- "/lessons-learned-for-cord19-deploying-your-computation-infrastructure-24378b828604"

---

Before I have [submitted task](https://medium.com/@alex.mikhalev/building-knowledge-graph-from-covid-medical-literature-kaggle-cord19-competition-f0178d2a19bd), I lost data more than once, so for next phase, I decided to start from the bottom up: roll out you own in-memory storage (Redis cluster) and own Database/block storage.

Overall conclusion: Try Nomad/Consul before going Kubernetes.

Why not use off-the-shelf managed Redis or Azure Cache? Looking at prices for in-memory cache in MBs/dollar and SQL compatible storage quotas doesn’t encourage: I am not enterprise, for me, this is “night” project between kids sleeping, and I am falling, so the budget is limited to what I can spin for free credits. Good news I have free credits in Azure/Google Cloud and free tier in AWS. I also got so fed up with losing data I purchased Hetzner Dedicated server with 4 TB disks. Overall credits are limited 90 GBP in Azure, ~250 in Google Cloud, Free tier in AWS, combined should give me enough of processing and storage. Individually I will max out credits in any cloud in a week. Why?

- Redis: I run out of memory on 32 GB dedicated server — overall size of the in-memory dataset (optimised) is about 40 GB. I can do more with Redis (Redis cbloom, RedisGraph), but I definitely will max out high mem instance. Also, cloud memory optimised instances have smallish storage. Fortunately, the Redis Cluster seems to be easy to install and fits requirements.
- PostgreSQL: I don’t have preference PG vs MySQL, I only use select and temp table, but I think the database is needed if you want to process text in parallel: I run out of space on Azure instance when I tried to dump sentences into plain tab CSV — 90GB text file. Default GCP SQL instance has about 40 GB storage, need to fill forms to enable more. GCP has a lot of features about managing instances inside the platform, adding hetzner server into the mix seems to be a quite involved job (and hetzner my data swamp)
- Moving large CSV files around even zipped doesn’t encourage me (did you know Google SQL import doesn’t accept zipped SQL/CSV files? How do they think dumps arrive into google bucket?). Moving files around should be taken care of by infrastructure automagically. I have considered storing sentences in parquet with snappy compression, but again — with storing text, this is a job for the database(ish) replica.

### Path has taken

1. Zerotier as VPN/network plane. I want all instances and servers be part of VLAN and I don’t want to think about managing/securing network and setting firewalls. This is a very mature product and I have a[n ansible playbook](https://github.com/m4rcu5nl/ansible-role-zerotier) to add the node to my network. Works like the charm.
2. PostgreSQL (debatable). I have ansible-playbook to roll out pg instance and secure it to Zerotier. Works, but replicas don’t. May be if I would start again I will look into deploying [TiDB](https://github.com/pingcap/tidb) — horizontally scalable Mysql compatible database.

In the past, I would use Riak and Riak CS to do the job, however, some time ago Basho made rather questionable decision to incorporate Solr into their product. Which doesn’t make sense from my perspective: why do I want to deploy java with 400MB RAM requirements just to start addon, when to deploy main product takes 40 MB RAM and runs on Erlang? I have used Riak in production in Shopitize, I may come back to it.

So what is the trendy tool to deploy computation jobs (orchestrate) across multiple clusters with occasion persistence? Mpi? Dask? Of cause modern tool is Kubernetes!

So, requirements:

- Easy maintenance
- Redis cluster on top
- Storage on top
- Secure network over Zerotier
- Multi-cloud

Base image: Ubuntu 18.04

The best recipe I manage to find is [here](https://www.notion.so/Kubernetes-cluster-5afa444ba9364db881e2a1cd51f9c069#65329b33946943dfb35d52441434d763), which is where I got closest to implement Kubernetes cluster with Hetzner server and Azure/AWS instance. I manage to have a working master and joined node, I even managed to get [Minio](https://min.io/) deployed, but only working on one node and using only one storage. I blamed it for leftovers of MicroK8s on master node (hetzner, unlike AWS in article). Minor amendment:

> sudo apt-get install -y docker.io kubelet kubeadm kubectl kubernetes-cni

Observation: Vanilla and most popular Kubernetes k8s installation built for Ubuntu 16.04.6. Current most common Ubuntu LTS 18.04 and week ago Ubuntu rolled out 20.04 LTS.

### Learnings from first go

[Kube-router](https://www.kube-router.io/) is an amazing product and good direction of travel for Kubernetes ecosystem.

### Next step:

In the past, I used [Rancher](https://rancher.com/) quite successfully in the past to deploy docker/Kubernetes and I had a good experience with it. I also found a few Rancher projects which would fit my requirements: [Longhorn](https://longhorn.io/) and [Submarine](https://rancher.com/blog/2019/announcing-submariner-multi-cluster-kubernetes-networking/).

So rancher server on hetzner box (I failed to deploy Rancher into local Kubernetes with connection to AWS RDS with some obscure error).

After several nights playing with Rancher/RKE, I would say RKE looks like a mature product with several options in beta/evaluation mode — like NFS provider, Longhorn and Submarine. It also has a set of [multi-cluster apps](https://rancher.com/docs/rancher/v2.x/en/catalog/multi-cluster-apps/), which is what you probably want to use Kubernetes for. Overall experience is better with RKE than with k8s, but despite multiple attempts and various configurations of master with different networks (weave for example) I didn’t manage to achieve working multi-cloud Kubernetes cluster. Once Rancher will start support kube-router it may be different.

### Lessons:

I had to dig deep into different network [CNI for Kubernetes](https://rancher.com/docs/rancher/v2.x/en/faq/networking/cni-providers/). Kubernetes is very opinionated about networks and always mess up installation despite zero tier network. The overall experience left me with the feeling that Kubernetes is not the right direction of travel for IT industry: it violates technology evolution rules: innovation is the drive towards simplicity in technology.

![](/post/img/2020-04-30_lessons-learned-for-cord19-deploying-your-computation-infrastructure_0.png#layoutTextWidth)

Kubernetes (and Tensorflow) are an example of products developed and tailored to very specific Google needs and infrastructure. It is great that Google is so proud of their engineering as to open source it. It is actually bad idea to use them outside of very specific they were developed for and it is a shame it’s so popular and people trying to use them forgetting decades of deployment practices: few more years and we will be able to do with Kubernetes what we were able to do 10+ years ago with VPN (cubed) over multiple clouds. Also did ever wondered how SETI@HOME was architectured?

Price comparison for SQL: AWS RDS pricing is more favourable than Azure.

Price comparison for computing instance: for the price of Azure/AWS medium memory enabled instance you can get top high performance dedicated server.

Other interesting projects found:

[slackhq/nebula](https://github.com/slackhq/nebula "https://github.com/slackhq/nebula")[Traefik, The Cloud Native Edge Router | Containous](https://containo.us/traefik/ "https://containo.us/traefik/")

### What’s next? Try Nomad

When struggling to get Kubernetes working the way I wanted it, I stumble across Nomad and Kubernetes [comparison](https://www.codemotion.com/magazine/dev-hub/backend-dev/nomad-kubernetes-but-without-the-complexity/). And this [one](https://blog.nobugware.com/post/2019/nomad_an_alternative_to_kubernetes/). This is where I had an aha moment — what is the way to deploy docker (not only docker, other containers too) container on the server and run it? This is what Nomad was designed to do. And it plays nicely with Kubernetes. Hashicorp is known for the quality of their software, independent view and “right design” — both Consul and Nomad trying to leverage local system capabilities and allow to plug or run whatever you want alongside. I used Vagrant (with chef) in the past but then moved towards ansible (this is probably I should have stuck, instead of trying to use Kubernetes). Next week is going to learning Nomad and deploying something like [Open Faas on Nomad](https://www.hashicorp.com/blog/functions-as-a-service-with-nomad/). Which is not probably what I should be doing: I have way more ideas about using OWLready processed ontology, building Aho-Corasick automata directly from ontology, ranking nodes per article, but I am stubborn and I don’t want unfinished Gestalt. Stay tuned for the next post.

* * *
Written on April 30, 2020 by Alex Mikhalev.

Originally published on [Medium](https://medium.com/@alexmikhalev/lessons-learned-for-cord19-deploying-your-computation-infrastructure-24378b828604)
