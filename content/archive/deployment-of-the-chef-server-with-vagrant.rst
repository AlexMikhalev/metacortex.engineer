Deployment of the chef server with vagrant
##########################################
:date: 2010-10-26 16:39
:author: Alex
:tags: blog, general, ruby, web

Some time ago I started playing with excellent tool vagrant. In this
post I will show how to setup chef server using vagrant.

Preliminaries

--------------

I assume that you know what is vagrant
[vagrant](http://www.vagrantup.com "Vagrant") and chef
[opscode](http://www.opscode.com/chef/ "Chef")

Issues

One of the problems with chef that it depends on unique hostname.
Vagrant discussion
[ticket](http://github.com/mitchellh/vagrant/issues/issue/139/#comment\_373819
"Ticket"), suggests that it's job of the provisioner to setup hostname.
But if you tried to use chef to change hostname in two step:

\* change hostname

\* change domainname

as I tried initially, chef will breaks between those two steps.

Following example on [agiletesting](http://agiletesting.blogspot.com
"Agile Testing").

I wrote a small \`hosts:chefserver\` receipt, available on
[github](http://bit.ly/d5POYH "Github"), which changes hostname and
domain name in one go using \`node\_name\`.

.. raw:: html

   <p>

::

    #!/bin/bashHOSTNAME=$1hostname $HOSTNAMEecho $HOSTNAME> /etc/hostnameIPADDR=`ifconfig  | grep 'inet addr:'| grep -v '127.0.0.1' | cut -d: -f2 | awk '{ print $1}'`echo $IPADDR >/tmp/ip_currentsed -i "s/127.0.0.1[[:space:]]localhost/127.0.0.1    localhost\n$IPADDR  $HOSTNAME.scilogonline.com $HOSTNAME\n/g" /etc/hostssed -i "s/127.0.1.1 vagrantup.com   vagrantup/$IPADDR  $HOSTNAME.scilogonline.com $HOSTNAME\n/g" /etc/hosts

.. raw:: html

   </p>

And full vagrant code for test deployment of chefserver:

.. raw:: html

   <p>

::

       config.vm.define :chefserver do |chefserver_config|     chefserver_config.vm.box="base"    chefserver_config.vm.provisioner=:chef_solo    chefserver_config.vm.forward_port("chefs", 4000, 4000)    chefserver_config.vm.forward_port("chefs_web", 4040, 4040)      chefserver_config.vm.forward_port("ssh", 22, 2223,:auto => true)       chefserver_config.chef.node_name="chefserver"    chefserver_config.chef.cookbooks_path = ["cookbooks","other_cookbooks"]    chefserver_config.chef.run_list.clear    chefserver_config.chef.add_recipe("hosts::chefserver")    chefserver_config.chef.add_recipe("apt")    chefserver_config.chef.add_recipe("build-essential")    chefserver_config.chef.add_recipe("chef::bootstrap_server")    chefserver_config.chef.json.merge!({       :chef=> {        :server_url=> "http://chefserver.*.com:4000",        :webui_enabled=> true,       }      })   end

.. raw:: html

   </p>

