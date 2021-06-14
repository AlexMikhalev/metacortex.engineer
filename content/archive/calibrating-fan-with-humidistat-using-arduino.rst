Calibrating cheap fan with Analog Humidistat using Pinoccio (Arduino-compatible board) and DHT22 sensor
#######################################################################################################
:date: 2015-11-27 12:14
:author: Alex
:tags: arduino, pinocio, geek, dht22, humidity, home automation, internet of things, iot

I bought cheap bathroom fan to tackle common in Britain mold problem in a bathroom and it comes with analog humidistat, which you can adjust using screwdriver. My goal is to make sure my fan switches off on 50% humidity or lower. 

I had a two Pinoccio boards and DHT22 laying around and decided to make use of them. Plugged DHT22 to into D4 hole (Ground and +3.3 V as required) into Field Scout and uploaded:

https://gist.github.com/AlexMikhalev/a49d35c6a18ffe74a266

Check serial port is working:


.. code:: bash

	Hello from Pinoccio!
	(Shell based on Bitlash v2.0 (c) 2014 Bill Roy)
	Custom Sketch (rev unknown)
	14652 bytes free
	Field Scout ready

	>dht22.report
	23.00
	52.80
	{"type":"custom","name":"dht22","custom":["{\u0022dht22.temperature\u0022:23, \u0022dht22.humidity\u0022:52}"],"at":6377}
	{"dht22.temperature":23, "dht22.humidity":52}



Pinocio HQ is struggling to work, so we need a local server to capture response:

http://support.pinocc.io/hc/en-us/articles/203183340-Run-Your-Own-Pinoccio-Server

.. code:: shell

	> npm install -g pinoccio
	> npm install --save pinoccio-server
	>node server.js


Connect to Lead Scout via serial console and redirect to new gateway:

.. code:: shell

	hq.setaddress("YOUR_IP_HERE"); wifi.dhcp; wifi.reassociate;

.. code:: shell

	function startup {hq.setaddress("YOUR_IP_HERE"); wifi.reassociate;}


Now command field scout to report to HQ:

.. code:: shell

	command.others("hq.report(\"dht22.report\",dht22.report);")


Now since hq.pinocc.io doesn't work properly for a while and node local server doesn't allow to type commands I am using 
https://raw.githubusercontent.com/luvit/luvit/master/examples/tcp-uv-proxy.lua instead of node.js serves.

Next post would be trying Scout proxy in different languages: D, Lua, Luv(Lua), Erlang, Python. 

