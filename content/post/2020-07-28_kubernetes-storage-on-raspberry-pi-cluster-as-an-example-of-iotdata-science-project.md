---
title: "Kubernetes storage on Raspberry PI cluster as an example of IoT/Data Science project"
author: "Alex Mikhalev"
date: 2020-07-28T19:23:47.735Z
lastmod: 2021-06-11T09:59:57+01:00

description: ""

subtitle: ""




aliases:
- "/kubernetes-storage-on-raspberry-pi-cluster-as-an-example-of-iot-data-science-project-8a0a1b16d64a"

---

Over the past few weekends, I have been distracted: I looked at Kubernetes storage in the past (got minio installed on Libreelec), and recently Longthorn announced GA — the project I am keen to explore. I got RPi4 B with 8GB Ram, which is the most powerful personal computer in the house, so I could not resist creating three nodes cluster — Raspberry PI 3B 2GB RAM, RPI 4B 4 GB RAM and RPI 4B 8 GB RAM and see if I can roll out Kubernetes (success) with distributed storage (not so).

My requirements towards those types of systems were shaped over ten years ago by a project called LeoNet practically useful IoT/Data Science even before such terms were fashionable. The scenario is quite typical: you have a bunch of Edge nodes (calling them Edge in IoT terms, not in Cloud terms), they have an expensive piece of equipment aerosol LIDAR attached to it, and some form of current RPI 3 equivalent (i386 Pentium), node deployed somewhere in the rural area and have some basic upload capability and generates not much — about 300–600 MB per hour. There is a central “system” which collects, processess and visualises measurement, it can be cloud-based, or it can be a dedicated server, an important point — it’s the ever-growing dataset, you start small with a single node. You add few more when you have 70 nodes and processed measurements for a few weeks you learn all sorts of optimisations for storing measurements: losing measurements is not an option. A node can be unreliable, but as soon as it sent measurements they are gold — you can’t go back in time and re-request clouds to be back in shape, for example, aerosol LIDARs picked up ash distribution after Eyjafjallajökull volcano eruption in 2010, obviously not a replicable event. I had a lot of pain managing storage, and as usual, data science projects don’t have a budget for server hardware. I ended up using XtreemFS (now defunct) and then just plain hdf.h5 over NFS. When we closed the project, it took over a month to the team to even attempt to download data over ASDL into their office. I think after a month of downloads they just gave up (and I believe the total volume was 4–5 TBs, desktop NAS by modern standards).

Most of the useful data science projects have similar requirements with a variation. So when I look at new technologies, my lens: with all advances in technology — hardware and software will it help me to achieve the same goal with less pain? Surprisingly the answer over the last at least three years is “no”.

How can you simulate measurements and the importance of keeping them stored reliably using unreliable hardware? We all now have it — family photos. To my wife’s (dismay? horror?) I use family photos as the testing dataset for my Kubernetes storage cluster. We have about 400GB of photos, and they are replicated in iCloud and Dropbox, but what if those cloud providers go bust or mess up the storage? You can’t go back in time to re-take photos of the kids or visit the places you have travelled t

We have 3 RPi; the first step is to install OS. Surprisingly Raspberry OS is the only arm32. Also, Longhorn requires iscisi driver, so I bootstrapped Ubuntu 20.04 and 18.04 (RP3).

OS Rant On: you can’t even boot 18.04 image from official Ubuntu page from the [official link](https://ubuntu.com/download/raspberry-pi) on RPI4, despite blog posts stating RPi4 support, there is a bug in the kernel which prevents booting on modern RPi4, and raspbian only have arm32. Ubuntu 20.04 has a nasty bug in cloud-init (known and reported) which forces you to type password 20 times before you will be able to login into ssh. Fortunately, [the kind person created an unofficial working 18.04 image](https://jamesachambers.com/raspberry-pi-4-ubuntu-server-desktop-18-04-3-image-unofficial/) — the real value of open-source, vendor dropped the ball, and community member stepped in to fix it. I found the Ubuntu approach strange, and I will avoid using Ubuntu in IoT devices going forward — the purpose of devices is to get stuff done, not “be-connected”). The best and most responsive image is [Gentoo RPi64](https://github.com/sakaki-/gentoo-on-rpi-64bit). /os rant off

I did manage to get k3s cluster working following [this tutorial](https://blog.alexellis.io/test-drive-k3s-on-raspberry-pi/) with a bit of [this](https://medium.com/@alexellisuk/walk-through-install-kubernetes-to-your-raspberry-pi-in-15-minutes-84a8492dc95a), what’s good — you can bootstrap Kubernetes in half-hour (although none of the install scripts k3s or k3sup appends cgroups to ‘/boot/cmdline.txt’, so you have to remember manually add it to /boot/cmdline.txt (although file path is different for 20.04 and 18.04). What’s good about it: you can run open faas on 3 RPi in minutes.

Next step for me to add rancher server — I like their UI and Longhorn, Longhorn UI can pickup authorisation from Rancher proxy auth removing the need for separate auth configuration.

Surprisingly while k3s supports arm64 only specific rancher version supports arm64–2.5.5 Fixme. And while I manage to start deployment of Longhorn, the deployment failed as Longhorn isn’t supported on arm64 — and it’s quite a strange combination — some parts do work on arm64, adding to the confusion. There are a ticket and PR waiting to be merged to have arm64 support in Longhorn, but it seems to be a lower priority for the team, which I find strange — Rancher announces their IoT support very publically.

I tried to use [Edge FS](http://edgefs.io/) out of [rook.io](https://rook.io/docs/rook/v1.0/edgefs-storage.html) project, but it doesn’t look like a mature project and it didn’t like block devices which ubuntu create for snaps — failed on bootstrap.

### Checklist to deploy Kubernetes on RPi (using Gentoo RPi4):

- [ ] In cmdline.txt add cgroup_enable=cpuset cgroup_memory=1 cgroup_enable=memory
- [x] enable wifi and eth0 — see [startup.sh](http://startup.sh)
- [x] ssh-copy-id to node (`ssh-copy-id -i ~/.ssh/id_rsa.pub [alex@192.168.1.](<mailto:alex@192.168.1.244>)110`)
- [ ] set the separate hostname for each node `nano -w /etc/conf.d/hostname` and `/etc/hosts`
- [ ] start k3s server on master
- [ ] Add first node: k3sup join — ip 192.168.1.244 — server-ip 192.168.1.122 — user alex
- [ ] add second node

Example of the server install k3sup

```
export SERVER_IP=192.168.1.244
export USER=pi

k3sup install \
  --ip $SERVER_IP \
  --user $USER \
 --k3s-extra-args '--docker' \
  --cluster
```

If config creation failed on the step above:

```
#get config
k3sup install --skip-install --ip $SERVER_IP   --user $USER   --cluster
export KUBECONFIG=/home/alex/kubeconfig
kubectl get node -o wide
```

Add node

```
export USER=alex
export SERVER_IP=192.168.1.244
export NEXT_SERVER_IP=192.168.1.122

k3sup join \
  --ip $NEXT_SERVER_IP \
  --user $USER \
  --server-user pi \
  --server-ip $SERVER_IP \
  --server
```

And another

```
export USER=alex
export SERVER_IP=192.168.1.244
export NEXT_SERVER_IP=192.168.1.122

k3sup join \
  --ip $NEXT_SERVER_IP \
  --user $USER \
  --server-user pi \
  --server-ip $SERVER_IP \
  --server
```

Install Kubernetes Dashboard

```
arkade install kubernetes-dashboard
```

Create RBAC auth

```
cat <<EOF | kubectl apply -f -
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kubernetes-dashboard
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kubernetes-dashboard
---
EOF
```

Get token

```
kubectl -n kubernetes-dashboard describe secret $(kubectl -n kubernetes-dashboard get secret | grep admin-user-token | awk '{print $1}')
```

start Kube proxy and visit `[http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#/node?namespace=default](http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#/node?namespace=default)`

To test deployment of resources — deploy open faas and minimal microservice — figlet from [here](https://blog.alexellis.io/test-drive-k3s-on-raspberry-pi/)

Apply minio operator and minio instance:

```
curl -O https://raw.githubusercontent.com/minio/minio-operator/master/examples/minioinstance.yaml
code minioinstance.yaml
kubectl apply -f minioinstance.yaml
```

Watch deployment fails: minio needs to be re-compiled for arm64 architecture — I know how to do it, but it will be in the next post.

So far Kubernetes on arm is only capable of running OpenFaas — which is an amazing project, but without storage, usefulness is very limited “we get paid for side effects” (quote from some functional programming discussion).

### Conclusion

The choice of Kubernetes storage drives a selection of all other components: hardware — arm64 or amd64, host operating system — ubuntu vs centos/RedHat and then Kubernetes variant. It seems too tight coupling for my liking, let’s hope at least one of the above projects will mature so I can replicate data science project from 10 years ago.

* * *
Written on July 28, 2020 by Alex Mikhalev.

Originally published on [Medium](https://medium.com/@alexmikhalev/kubernetes-storage-on-raspberry-pi-cluster-as-an-example-of-iot-data-science-project-8a0a1b16d64a)
