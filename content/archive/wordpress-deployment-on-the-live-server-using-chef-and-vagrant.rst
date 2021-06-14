Wordpress deployment on the live server using chef (and vagrant)
################################################################
:date: 2010-10-26 19:11
:author: Alex
:tags: blog, cloud, general, linux, ruby, web

When I decided to move from movable type to wordpress, I wasn't quite
happy with default wordpress cookbook. I also had an offer to have a
cheap dedicated server instead of VPS, so I decided to test two things
simultaneously:

\* Preparation of new live server using fabric

\* Deployment of new wordpress installation using chef with opscode
server

\* And of cause testing wordpress cookbook on vagrant

Here is how I do it:

Wordpress cookbook modifications

----------------------------------

let's start from wordpress cookbook. I don't quite like default
configuration with apache and php exposed directly to user. So I want to
put a nginx in front of it.

You can skip to cookbook directly at
[github](http://github.com/AlexMikhalev/cookbooks/tree/master/wordpress/
"Wordpress"), but it's very easy to do it in chef. Apache goes to port
8080:

.. raw:: html

   <p>

::

    node[:apache][:listen_ports]=[ "8080","443","8200"]node[:apache][:keepalive] = "Off"     include_recipe "apache2"include_recipe "apache2::mod_rewrite"include_recipe "apache2::mod_expires"include_recipe %w{php::php5 php::module_mysql php::module_curl}

.. raw:: html

   </p>

This seems to be a better way of adding ports:

.. raw:: html

   <p>

::

    node[:apache][:listen_ports] << "8080" unless node[:apache][:listen_ports].include?("8080")

.. raw:: html

   </p>

Disable default website:

.. raw:: html

   <p>

::

      execute "disable-default-site" do  command "sudo a2dissite default"  notifies :reload, resources(:service => "apache2"), :delayedend

.. raw:: html

   </p>

this is borrowed from vagrant cookbook. My webserver should be up and
properly configured or should be down then external monitoring tools
will alert me. I consider default page with "It works" as one of the
potential undetectable screw ups.

Adding nginx to installation is a peace easy:

.. raw:: html

   <p>

::

       # Make proxy with nginx include_recipe "nginx::default"# node[:nginx][:user]="www-data"template "#{node[:nginx][:dir]}/sites-available/wordpress.conf" do  source "nginx_proxy.conf.erb"  owner "root"  group "root"  mode "0644"  variables(    :app => "wordpress",    :docroot => node[:wordpress][:dir],    :server_name => "wordpress.#{node[:domain]}",    :server_aliases => node[:fqdn]  )end

.. raw:: html

   </p>

I felt entertained to add some more to wordpress installation, following
[link](http://tech.nocr.at/tech/how-to-speed-up-wordpress-with-nginx-and-wp-super-cache/).
My chef cookbook will produce two more configuration files:
\`wordpress\_proxy.conf\` in apache and nginx sites-available
directories. It is very unlikely that I will ever need any of those:
nginx used as load balancer to apache acting as proxy, see
\`freak\_proxy\_nginx.conf.erb\` for details.

Vagrantfile excerpts used for testing:

.. raw:: html

   <p>

::

         config.vm.define :web do |web_config|    web_config.vm.box = "base"     web_config.vm.provisioner = :chef_server         web_config.chef.chef_server_url = "https://api.opscode.com/organizations/"    web_config.chef.validation_client_name = "*-validator"    web_config.chef.validation_key_path = "/Users/*/Dropbox/chef_opscode/client-config/validation.pem"    web_config.chef.run_list.clear # Node name  web_config.chef.node_name = "wordpress"    web_config.chef.add_recipe("wordpress")    web_config.chef.add_recipe("monit")    web_config.vm.forward_port("web", 80, 1080)    web_config.vm.forward_port("web_no_proxy", 8080, 8082)    web_config.vm.forward_port("ssh", 22, 2222,:auto => true)  end

.. raw:: html

   </p>

Once I was sure wordpress will light up using my cookbook I uploaded it
to opscode server.

Prepare server for chef using fabric

-------------------------------------

Next step would be to prepare a ubuntu lucid minimal server I got from
hetzner.de. As I am lazy I use fabric for it.

Note that I use dev version of fabric. Here is a fabfile.py.

.. raw:: html

   <p>

::

     # This is configuration script for bootstraping chef and wordpress config(fab_hosts = ['IP_address'],fab_user='myname',root='/home/myname/',) def get_stat():    """ Test"""    run('uname -a')      def prepare_debian():    """Prepare debian/ubuntu for chef installation"""    sudo("""    apt-get update    aptitude -y install ruby ruby1.8-dev libopenssl-ruby1.8 rdoc ri irb build-essential wget ssl-cert    wget http://production.cf.rubygems.org/rubygems/rubygems-1.3.7.tgz    tar xvfz rubygems-1.3.7.tgz    cd rubygems-1.3.7    ruby setup.rb    ln -sfv /usr/bin/gem1.8 /usr/bin/gem    """)def install_chef():  """Install chef client"""  sudo("gem install chef")  sudo("""        mkdir -p /etc/chef    chown myname /etc/chef    """)  put("/Users/*/Dropbox/chef_opscode/client-config/client.rb","/etc/chef/client.rb")  put("/Users/*/Dropbox/chef_opscode/client-config/validation.pem","/etc/chef/validation.pem")  put("client_bootstrap.json","/etc/chef/client_bootstrap.json")  bootstrap_client()  def bootstrap_client():  """Bootstrap chef client"""  sudo("""  chef-client -j /etc/chef/client_bootstrap.json -L /var/log/chef.log -l debug  """)  def run_client():    """Runs chef client in debug mode"""    sudo("chef-client -L /var/log/chef.log -l debug")     def remove_validate():    """Removes chef validation.pem"""    sudo("rm /etc/chef/validation.pem")def update_hostname(hostname=None,domain="domainname.com"):    """Updates hostname"""    put("update_hostname","update_hostname")    sudo("""    mv update_hostname /usr/bin/    chmod +x /usr/bin/update_hostname    """)    sudo('update_hostname %s %s' % (hostname,domain))def update_dns(hostname=None):    """Update Dynamic DNS using wget"""    run("wget -q http://update.dnsexit.com/RemoteUpdate.sv?login=%%%&password=%%%&host=%s" % hostname)

.. raw:: html

   </p>

The way it works:

.. raw:: html

   <p>

::

    fab prepare_debianfab update_hostname:YOURFQDNfab install_cheffab remove_validate

.. raw:: html

   </p>

Add new recipe to new node using knife:

.. raw:: html

   <p>

::

      knife node run_list add NODE 'recipe[getting-started]'   fab run_client

.. raw:: html

   </p>

and very final to update DNS server:

.. raw:: html

   <p>

::

    fab update_dns:FQDN

.. raw:: html

   </p>

I made several mistakes during deployment and still had to login to
server using ssh. I noticed the drawback of using chef for real server -
you can't reset real server to default state as easy as VM. Another
drawback is that "ubuntu" or "apt" cookbooks removed providers proxy for
apt packages and they now fetched from US location.

My current TODO for cookbooks:

\* add charset to mysql cookbook.

\* add monit profiles to nginx/apache/postfix/mysql

\* make ssh keys distribution and sudoer group automatic

\* edit default postfix configuration

But I think I will wait till new server to arrive, as this is my hobby
rather then a job.
