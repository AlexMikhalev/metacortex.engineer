Monitoring rabbitmq server 2.5.1.  with monit
#############################################
:date: 2011-07-15 18:20
:author: Alex
:tags: cloud, linux

Simple task like setting up monitoring with monit for rabbit mq include
two parts:

1) As discussed `here`_ Modify /etc/init.d/rabbitmq-server



.. code:: bash

    The following are added to the start 
    function:   
    	pid=`/usr/sbin/rabbitmqctl status | perl -n -e'/{pid,(\d+)/ && print $1'`   
    	echo $pid > /var/run/rabbitmq.pid 
    	Right before:   
    	echo SUCCESS The pid file is deleted within the stop function:
    	          rm /var/run/rabbitmq.pid right after,          
    	          if [ $RETVAL = 0 ] ; then




2) Add this to monit configuration file:

.. code:: bash


    ### rabbitmq-server
	check process rabbitmq-server with pidfile /var/run/rabbitmq.pid     
	group rabbitmq     
	start program "/etc/init.d/rabbitmq-server start"     
	stop program "/etc/init.d/rabbitmq-server stop"     
	if failed port 5672 type tcp then restart     
	if 3 restarts within 3 cycles then timeout
	
	
    

.. _here: http://groups.google.com/group/rabbitmq-discuss/browse_thread/thread/b6bd0f50e962e43
