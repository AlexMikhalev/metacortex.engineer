Network misconfiguration
########################
:date: 2009-09-06 02:16
:author: Alex
:tags: network

[root@localhost ~]# traceroute -I ya.ru

traceroute to ya.ru (213.180.204.8), 30 hops max, 40 byte packets

1 217.23.185.153 (217.23.185.153) 1.059 ms 1.250 ms 1.470 ms

2 217.23.188.57 (217.23.188.57) 13.038 ms 13.631 ms 13.931 ms

3 192.168.224.17 (192.168.224.17) 20.346 ms 21.685 ms 22.524 ms

4 87.226.228.101 (87.226.228.101) 44.413 ms 45.105 ms 48.300 ms

5 ae-2.m7-ar1.msk.ip.rostelecom.ru (87.226.133.93) 50.622 ms 52.475 ms
52.885 ms

6 79.133.94.58 (79.133.94.58) 49.800 ms 50.031 ms 52.786 ms

7 silicon-vlan901.yandex.net (77.88.56.125) 53.076 ms 42.018 ms 42.207
ms

8 ortega-vlan4.yandex.net (213.180.210.188) 43.344 ms 38.884 ms 39.002
ms

9 ya.ru (213.180.204.8) 37.806 ms 38.778 ms 39.009 ms
