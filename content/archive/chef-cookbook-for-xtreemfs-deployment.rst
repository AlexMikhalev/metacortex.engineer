Chef cookbook for xtreemfs deployment
#####################################
:date: 2010-12-10 09:14
:author: Alex
:tags: cloud

I just pushed xtreemfs cookbook to my `git repo`_

This cookbook automates xtreemfs `quick start`_ for ubuntu 10.04.

I am using it with vagrant:

.. raw:: html

   <p>

::

       config.vm.define : xtreemfs do |xtreemfs_config|     xtreemfs_config.vm.box="base"    xtreemfs_config.vm.provisioner=:chef_solo    xtreemfs_config.vm.forward_port("ssh", 22, 2227,:auto => true)       xtreemfs_config.vm.forward_port("web", 30638, 8080)    xtreemfs_config.vm.network("192.168.100.16")    xtreemfs_config.chef.node_name="xtreemfs"    xtreemfs_config.chef.log_level = :debug     xtreemfs_config.chef.cookbooks_path = ["cookbooks","other_cookbooks"]    xtreemfs_config.chef.run_list.clear    xtreemfs_config.chef.add_recipe("apt")    # xtreemfs_config.chef.add_recipe("tomcat")     xtreemfs_config.chef.add_recipe("xtreemfs::server")    xtreemfs_config.chef.add_recipe("xtreemfs::client") end

.. raw:: html

   </p>

.. _git repo: http://github.com/AlexMikhalev/cookbooks
.. _quick start: http://www.xtreemfs.org/quickstart.php
