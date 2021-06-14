---
title: "Creating Redis Cluster from sticks and stones: Ansible based cross-cloud deployment"
author: "Alex Mikhalev"
date: 2020-05-13T13:27:21.112Z
lastmod: 2021-06-11T09:59:36+01:00

description: ""

subtitle: ""




aliases:
- "/creating-redis-cluster-from-sticks-and-stones-ansible-based-cross-cloud-deployment-38d925b44717"

---

First, I already had a two stopped Azure instances and ansible inventory file:

```
cat myazure_rm.yaml
plugin: azure_rm
include_vm_resource_groups:
- cord19demo
auth_source: cli

keyed_groups:
- prefix: tag
  key: tags(base)
```

Two other instances I created manually by hands and corresponding inventory file:

```
all:

hosts:

children:

redis_cluster:

hosts:

redis1AzureVM:

ansible_ssh_host: {{public_ip_address}}

ansible_ssh_port: 22

ansible_ssh_user: "alex"

ansible_ssh_private_key_file: "/home/*"

redis2AzureVM:

ansible_ssh_host: {{public_ip_address}}

ansible_ssh_port: 22

ansible_ssh_user: "alex"

ansible_ssh_private_key_file: "/home/*"

#FIXME: formatting above botched
```

Check that both inventory files working properly:

```
ansible all -m ping -i myazure_rm.yaml
ansible all -m ping -i postgresql/azure_instance.yaml
```

Assign all nodes into the same zerotier network:

```
$ ansible-playbook  -i ./myazure_rm.yaml  ./zerotier-play.yaml
$ ansible-playbook  -i ./azure_instance.yaml  ./zerotier-play.yaml
```

And where is my hetzner box? Ah, in the wrong network.

```
ansible-playbook  -i ./postgresql/development.yaml  ./postgresql/zerotier-play.yaml
```

Create two GCP instances

```
ansible-playbook create_gce_vm_corrected.yml 
ansible-playbook create_gce_vm_corrected2.yml
```

see the previous post for the code samples. Check we are up:

```
ansible all -m ping -i instances.gcp.yml
```

And enroll GCP nodes into the same Zerotier network:

```
ansible-playbook  -i instances.gcp.yml  ./zerotier-play.yaml
```

And get list of all nodes from Zerotier:

```
$ curl -s -v --header "Authorization: bearer {{auth_token}}"  https://my.zerotier.com/api/network/{{network_id}}/member | jq . > network_list.json 
$ jq ".[] | .config | .ipAssignments[0]"  network_list.json

"10.144.101.190"
"10.144.211.47"
"10.144.83.129"
"10.144.133.112"
"10.144.15.164"
"10.144.175.223"
"10.144.109.149" 
```

now I have a list of IP addresses of all my nodes. And it was only warm-up, interesting part starts.

Create docker redismod.yml grab it from [Gist](https://gist.github.com/AlexMikhalev/3aca3a5a0560c4d542692015bf6016d5). Why docker based Redis deployment? Current modules not playing well together with default vendor (Ubuntu) based Redis and also it’s very not trivial to change default dir using system conf. Wrapping it all into one docker makes it easy to deploy.

See gist and also create template:

```
cluster-enabled yes
cluster-config-file nodes.conf
cluster-node-timeout 5000
appendonly yes
dir /data
bind {{ ansible_ztnfallfvg.ipv4.address }}
loadmodule /usr/lib/redis/modules/redisearch.so
loadmodule /usr/lib/redis/modules/redisgraph.so
loadmodule /usr/lib/redis/modules/redisbloom.so
loadmodule /var/opt/redislabs/lib/modules/redisgears.so
stop-writes-on-bgsave-error no
```

Template relies on zerotier IP address and also docker started with “host” network. Zerotier network interface name is a network-specific, so you may have to change {{ ansible_ztnfallfvg }} in redis.conf and in docker yaml. (check ifconfig or ansible network debug information).

Just to make sure all 7 nodes have same Redis conf and redis:

```
ansible-playbook  -i ./myazure_rm.yaml -i instances.gcp.yml -i ./development.yaml -i ./azure_instance.yaml docker_redismod.yml
```

If something broke fix it :), I need to figure out better way to grab Zerotier IP address for ansible, but it will have to wait another day.

Now the missing bit: you have Zerotier network, nodes with Redis install, but you can’t ping or connect to nodes unless your machine is part of the same network. Join via zerotier cli or GUI, make sure Auth is ticked on my.zerotier.com.

Create redis cluster using redis-cli command or redis-trib.py (pip install redis-trib.py)

```
redis-cli --cluster create 10.144.15.164:6379 10.144.133.112:6379 10.144.83.129:6379 10.144.211.47:6379 10.144.109.149:6379
```

I messed this part up — due to remains of old two nodes from previous Redis cluster deployment, so I had to spend a few hours recovering until I found a redis-trib.py rescue command

```
redis-trib.py rescue --new-addr 127.0.0.1:7004 --existing-addr 127.0.0.1:7000 
```

Next to get things actually done.

* * *
Written on May 13, 2020 by Alex Mikhalev.

Originally published on [Medium](https://medium.com/@alexmikhalev/creating-redis-cluster-from-sticks-and-stones-ansible-based-cross-cloud-deployment-38d925b44717)
