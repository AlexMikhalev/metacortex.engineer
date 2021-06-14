Evolving architecture
#####################
:date: 2016-01-11 12:00
:author: Alex
:tags: architecture, mongo, riak, node.js 

The role of the architecture is to support endless tickering and pivoting of the company. If we follow Goldratt idea that the goal of the company is to "make money now and in the future", "in the future" is the part which is supported by good architecture. 

The examples of the good architecture is International Space Station - although developed few decades ago, it is still going ahead with enourmous amount of tickering, small modification, while maintaining integrity, resilience and security of the inhabitats.

The evolution of the startup architecture can be viewed in 3 staging (assuming you are growing):

1. Single Server/single sight. Everything centralized and under company control. SaaS model works perfectly. The goal of the company on this stage to find product/market fit, paying customers etc. You are rewriting your code quite regularly in hope that at least 30% of it remains stable.

2. Once you hit a mark if you are not prepared you will get "slash dot effect", where overwhelmed by traffic your system is going down and you are loosing and reputation by not being able to serve the demand. If architure is done right, this is where the company makes a step to partially-distributed architecture: 
2.1 leveraging cludfront for static deliverables - closer to consumer
2.2 distributed services behind load-balancer - DNS and network based load balancing for spreading the load
2.3 Distributed databases and DR across multiple datacenters 
 
