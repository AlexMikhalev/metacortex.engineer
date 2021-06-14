Good way to ad apt repository using chef - from hadoop cookbook
###############################################################
:date: 2010-12-09 21:41
:author: Alex
:tags: cloud

I found an interesting way of adding apt repository in hadoop cookbook:

.. raw:: html

   <p>

::

    execute "apt-get update" do  action :nothingendtemplate "/etc/apt/sources.list.d/cloudera.list" do  owner "root"  mode "0644"  source "cloudera.list.erb"  notifies :run, resources("execute[apt-get update]"), :immediatelyendexecute "curl -s http://archive.cloudera.com/debian/archive.key | apt-key add -" do  not_if "apt-key export 'Cloudera Apt Repository'"end

.. raw:: html

   </p>

