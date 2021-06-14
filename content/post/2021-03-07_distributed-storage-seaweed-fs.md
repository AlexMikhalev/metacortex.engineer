---
title: "Distributed Storage: Seaweed FS"
author: "Alex Mikhalev"
date: 2021-03-07T09:32:50.609Z
lastmod: 2021-06-11T10:00:15+01:00

description: ""

subtitle: ""




aliases:
- "/distributed-storage-seaweed-fs-cce587ef79cf"

---

I came across [Seaweed FS](https://github.com/chrislusf/seaweedfs/wiki/Getting-Started), which I think is perfectly architectured:

- Acknowledgement of existence of other technologies, so master metadata can be stored in Redis(Cluster), Cassandra, Etcd
- Any use case I could think of covered — FUSE mount, HDFS, S3 API gateway, WebDAV, Async Backup into the cloud
- Tiered Storage.
- Cross-Datacentre replication (I don’t need it at home, but the number of databases/storages supporting cross DC replication out of the box can be counted on one hand)

Quickstart with a single master on one RPI4 server and volume server on another took 10 minutes. Why did I spend so much time going through edge fs, Ceph and Gluster FS? Now I need to figure out how to migrate GlusterFS to it, currently, I have 3 RPI4 nodes each with 128 GB USB stick and 1 TB external drives holding:

1. Docker volume — 3 replicas over 3 microSD cards
2. largerpivolumes — JBOD configuration in GlusterFS over all disks (12 TB)
3. Fastvolume — JBOD over usb sticks 337G
4. slow volume — replicate over 2 disks with one arbiter

Now I need to plan for 30 minutes to have the same volumes setup and more importantly figure out a way to move data from Gluster into seaweed fs.

The challenge: I don’t have a single large enough disk to hold all data. Any suggestions?

* * *
Written on March 7, 2021 by Alex Mikhalev.

Originally published on [Medium](https://medium.com/@alexmikhalev/distributed-storage-seaweed-fs-cce587ef79cf)
