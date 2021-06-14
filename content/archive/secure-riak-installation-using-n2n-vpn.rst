Secure Riak installation using n2n VPN
######################################
:date: 2011-07-08 09:22
:author: Alex
:tags: cloud, linux, web

Recently, I decided to have a closer look at `Riak`_ non-sql database,
but found out that unlike CouchDB riak doesn't have a HTTP basic auth
implemented, or any other way of defining secure access to database.

I have three servers to build a cluster, but I feel very uneasy leaving
open ports and full access to database to everyone in the world. The
best practice guide `here`_ lists all ports necessary to secure riak
installation, but messing with iptables didn't feel like compelling
idea.

So I decided to set up a VPN and only make riak nodes available on
internal network inside VPN. Again, system administration is my hobby
rather than the main job, so VPN installation should be straightforward
and simple.

That's how I found absolutely amazing product - `n2n`_ - Peer-to-Peer
VPN network.

I used svn version, but it is in standard ubuntu repos. I suggest
install n2n network first, then configure cluster later(obviously I did
it other way around,but you don't have to repeat my mistakes). I
successfully installed n2n on 3 Ubuntu Lucid 10.04.2 and Mac OS X
Leopard and Snow Leopard.

1) Step 1. Prepare supernode (Linux):

.. code:: bash

    sudo aptitude install uml-utilities 
	#user mode utilssudo tunctl -t tun0 
	# create tun0 interface
	sudo aptitude install quilt libssl-dev 
	#necessary libraries
	svn co https://svn.ntop.org/svn/ntop/trunk/n2n 
	#checkout trunk
	cd n2n/n2n_v1/make





So far everything straightforward.

Step2. Start supernode:

.. code:: bash


    ./supernode -l 1222 -v



"-v" indicate verbose output, supernode is a daemon, so no need to nhop
etc.

Step3. On any other machine (not supernode), for linux follow step 1,
create tun0 interface, then

.. code:: bash

    sudo ./edge -d tun0 -a new_node_internal_ip -c myVNPnetwork -k secretkey -l supernode_ip:1222 -v



For linux client "-d" is compulsory and should pass already created tun0
interface after that.

new\_node\_internal\_ip - new internal IP, my for example in range
10.0.\*.\*.

"-k secretkey" - you network encryption key. Should be common between
nodes.

Then most important part - wait. Looking at verbose output of supernode
and edge, edge should have:

.. code:: bash

    "Registering with supernode"Received REGISTER_ACK from remote peer [ip=*:1222]


for successful registration.

Every time when you shutdown/restart edge or supernode it takes some
time to re-register. Depending on the network it can take from few
seconds to a few minutes. If you shutdown supernode, all clients should
re-register, which can take up to 5 minutes.

Next repeat step 1 and 3 for other linux client for example. Do not try
to install edge client on supernode until you have at least two other
nodes and you can ping each other on internal ip. Replace "-v" with "-f"
once configuration is fully functional.

If you want to add Mac OS X client, install tun/tap driver for mac os
first from `here2`_, then

.. code:: bash


    sudo ./edge  -a new_node_internal_ip -c myVNPnetwork -k secretkey -l supernode_ip:1222 -v


no need to pass parameter "-d".

Now, assuming you have successfully installed at least two clients and
have pinged each other over internal network, adding supernode computer
as a node edge:

.. code:: bash

    sudo ./edge -d tun0 -a new_node_internal_ip -c myVNPnetwork -k secretkey -l supernode_ip:1222 -v -r


"-r Enable packet forwarding through n2n community" is important
parameter here and that was the only way how I manage to add edge on
supernode computer.

This is enforces all packets to go via supernode ( Usually supernode
acts only as an information exchange for other nodes, and encrypted
connection formed between two edges directly ( remember it's p2p
network), but routing becomes messy if you connect edge node on same
computer which runs supernode - other edge clients can't see edge
installed on supernode directly).

Supernode also acts as a router for a nodes behind NAT firewall.

All nodes should be fine and talking, we can go to `Basic Cluster
setup`_.

For linux:

.. code:: bash


    wget http://downloads.basho.com/riak/CURRENT/riak_0.14.2-1_amd64.debdpkg -i riak_0.14.2-1_amd64.deb sudo dpkg -i riak_0.14.2-1_amd64.deb



Then edit "/etc/riak/app.config" and "/etc/riak/vm.args", put new
(internal) IP addresses in appropriate places.

If you already had riak installation,

.. code:: bash

    sudo riak-admin reip riak@old_ip riak@new_ipsudo riak-admin remove riak@127.0.0.1



and on other new riak nodes:

.. code:: bash


    ./bin/riak-admin join riak@10.0.*.2


Now you should have a secure riak cluster and in my case it is also
spread across two datacenters and home. But you still may want to for `a
trial of Enterprise Riak`_ if you are serious about deploying riak in
production.

.. _Riak: http://www.basho.com/products_riak_overview.php
.. _here: http://wiki.basho.com/Network-Security-and-Firewall-Configurations.html
.. _n2n: http://www.ntop.org/n2n/
.. _here2: http://tuntaposx.sourceforge.net/
.. _Basic Cluster setup: http://wiki.basho.com/Basic-Cluster-Setup.html
.. _a trial of Enterprise Riak: http://info.basho.com/freetrial.html
