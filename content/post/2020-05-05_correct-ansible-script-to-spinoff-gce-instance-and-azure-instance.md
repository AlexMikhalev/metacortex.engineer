---
title: "Correct Ansible script to spin-off GCE instance and Azure instance"
author: "Alex Mikhalev"
date: 2020-05-05T18:21:12.674Z
lastmod: 2021-06-11T09:59:33+01:00

description: ""

subtitle: ""




aliases:
- "/correct-ansible-script-to-spin-off-gce-instance-and-azure-instance-af9320ffed3"

---

A surprisingly large number of Ansible examples/documentation require additional work before they can work as expected.

To spin off Google Cloud compute instance using ansible use [Gist](https://gist.github.com/AlexMikhalev/498224bd5928f6b8bf96d2a6bdf2cd9f) instead of official one [here](https://docs.ansible.com/ansible/latest/scenario_guides/guide_gce.html).

And if you want to spin Azure instance using Ansible use this [Gist](https://gist.github.com/AlexMikhalev/ebf3c65817774830821bb396a6708efe).

Next step to make dynamic inventory working

For Google Cloud create file:

```
plugin: gcp_compute
projects:
  - cord19kaggle
auth_kind: serviceaccount
service_account_file: "/home/alex/*.json"
```

For Azure

```
plugin: azure_rm
include_vm_resource_groups:
- cord19demo
auth_source: auto

keyed_groups:
- prefix: tag
  key: tags
```

> Use like: ansible-playbook -i instances.gcp.yml ./postgresql/zerotier-play.yaml

* * *
Written on May 5, 2020 by Alex Mikhalev.

Originally published on [Medium](https://medium.com/@alexmikhalev/correct-ansible-script-to-spin-off-gce-instance-and-azure-instance-af9320ffed3)
