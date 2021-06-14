Upgrading to Movable Type 5 using chef and vagrant
##################################################
:date: 2010-10-26 17:38
:author: Alex
:tags: blog, cloud, ruby

As a long time perl developer, I have admired Movable Type (mt). So
recently I decided to upgrade to MT5. In the end I decided to move from
movable type to wordpress, but this is my notes:

First I took chef's cookbook from wordpress and modified it so it will
install mt5 instead of wordpress. Then I learned that you can't backup
your data using MT4 and restore it in MT5, so I had to add installation
of mt4.

After seeing MT5, I decided to move to wordpress completely, so I didn't
finish movabletype cookbook - it have README about wordpress.

So for those who interested in testing it:

[MovableType](http://github.com/AlexMikhalev/cookbooks/tree/master/movabletype/
"Movable Type cookbook")

Note, that mysql cookbook requires that you use chef server in order to
store passwords after generation. So easiest way is to get chef server
is to register on opscode website (or use `previous post`_ for chef
server deployment).

Vagrant configuration for movable type:

.. raw:: html

   <p>

::

         config.vm.define :web2 do |web2_config|    web2_config.vm.box = "base"     web2_config.vm.provisioner = :chef_server    web2_config.chef.cookbooks_path =  ["cookbooks","other_cookbooks"]  web2_config.chef.node_name = "movabletype"    web2_config.chef.chef_server_url = "https://api.opscode.com/organizations/*"    web2_config.chef.validation_client_name = "*-validator"    web2_config.chef.validation_key_path = "/Users/*/Dropbox/chef_opscode/client-config/validation.pem"      web2_config.chef.run_list.clear    web2_config.chef.add_recipe("movabletype")    web2_config.vm.forward_port("web", 80, 8080)    web2_config.vm.forward_port("ssh", 22, 2222,:auto => true)  end

.. raw:: html

   </p>

This should start VM with two movable type installations available:

\`server\_fqdn+"/mt4/"

server\_fqdn+"/mt5/"\`

.. _previous post: http://sci-blog.com/2010/10/deployment-of-the-chef-server-with-vagrant/
