Quick way to bootstrap chef server with vagrant
###############################################
:date: 2010-08-26 06:24
:author: Alex
:tags: cloud, ruby, web

As a big fan of automatic software deployment and cloud computing, today
I tried [chef]("http://www.opscode.com/chef/") following several
tutorials
[one]("http://agiletesting.blogspot.com/2010/07/chef-installation-and-minimal.html"),
[two]("http://agiletesting.blogspot.com/2010/07/working-with-chef-cookbooks-and-roles.html")
and
[three]("http://www.themomorohoax.com/2010/07/31/ruby-chef-tutorial").
But because I am lazy, I decided to try to use vagrant to setup chef
server.

Vagrant is a absolutely amazing wrapper for Virtual Box and can
provision virtual machines on a spot using chef-solo or chef-server.

I have a lot of plans for vagrant+chef.

Lets start:

\* Download and install Oracle Virtual Box, OSE version would not work

\* install ruby and rubygems. Mine ruby 1.8.7 (2010-08-16 patchlevel
302) [i686-darwin10.4.0]), with gems 1.3.6 via rvm. I highly recommend
using rvm, as I had to drop 1.3.7 rubygems due to incompatibility with
chef's cookbooks. ( Possibly, now sorted)

.. raw:: html

   <p>

::

    gem install vagrant

.. raw:: html

   </p>

.. raw:: html

   <p>

::

    mkdir -p /ruby/Vagrantcd ~/ruby/Vagrant

.. raw:: html

   </p>

Following quickstart:

.. raw:: html

   <p>

::

     vagrant box add lucid32 http://files.vagrantup.com/lucid32.boxvagrant initvagrant up

,

.. raw:: html

   </p>

so my base box is lucid32

At this stage you should have virtual box and vagrant fully functional.

Now

.. raw:: html

   <p>

::

     git clone http://github.com/thewoolleyman/cookbooks.git other_cookbooks

.. raw:: html

   </p>

I tried to use official opscode cookbooks, but they currently have mysql
cookbook broken, which breaks wordpress cookbook and others I wanted to
play with.

Now add to Vagrantfile:

.. raw:: html

   <p>

::

    config.vm.define :chefs do |chefs_config|chefs_config.vm.box = "base"chefs_config.vm.provisioner = :chef_solochefs_config.chef.cookbooks_path = "other_cookbooks"chefs_config.chef.run_list.clearchefs_config.chef.add_recipe("apt")chefs_config.chef.add_recipe("build-essential")chefs_config.chef.add_recipe("chef::bootstrap_server")chefs_config.vm.forward_port("chefs", 4000, 4000)chefs_config.vm.forward_port("ssh", 22, 2223,:auto => true)chefs_config.chef.json={:chef=> {:server_url=> "http://localhost.localdomain:4000",:webui_enabled=> true,}}end

.. raw:: html

   </p>

Obviosly it should be between Vagrant::Config.run do \|config\| and end.

now

.. raw:: html

   <p>

::

    vagrant up chefs

.. raw:: html

   </p>

should start and provision chef server.

.. raw:: html

   <p>

logging into it using vagrant ssh chefs should allow to continue first
tutorial from

::

    "e) #knife configure -i"

.. raw:: html

   </p>

Alternative way to use chef server without installing your own is to
subscribe to opscode platform.

Vagrant configuration for this, using wordpress chef cookbook:

.. raw:: html

   <p>

::

    config.vm.define :web do |web_config|web_config.vm.box = "base"# config.vm.provisioner = :chef_soloweb_config.vm.provisioner = :chef_serverweb_config.chef.chef_server_url = "https://api.opscode.com/organizations/ORGANIZATION"web_config.chef.validation_client_name = "ORGANIZATION-validator"web_config.chef.validation_key_path = "/Users/*/Dropbox/chef_opscode/client-config/validation.pem"web_config.chef.run_list.clearweb_config.chef.add_recipe("wordpress")web_config.vm.forward_port("web", 80, 8080)web_config.vm.forward_port("ssh", 22, 2222,:auto => true)end

.. raw:: html

   </p>

Which is now gives virtual machine with wordpress install

.. raw:: html

   <p>

::

    vagrant up web

.. raw:: html

   </p>

Stay tuned for more articles featuring Dropbox, vagrant, virtual box and
possibly Pareto.

Update: There is a newer version of `the post`_

.. _the post: http://sci-blog.com/2010/10/deployment-of-the-chef-server-with-vagrant/
