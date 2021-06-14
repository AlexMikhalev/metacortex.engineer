Celery configuration for Redis backend
######################################
:date: 2010-11-13 19:30
:author: Alex
:tags: cloud, web

Not too obvious since doc
[here]("http://ask.github.com/celery/tutorials/otherqueues.html")
doesn't mention it.

Working configuration:

.. code:: python

    CARROT_BACKEND = "ghettoq.taproot.Redis"
	CELERY_RESULT_BACKEND = "redis"
	REDIS_HOST = "localhost"
	REDIS_PORT = 6379
	REDIS_DB = 0
	REDIS_CONNECT_RETRY = True #this one is deprecated
	BROKER_HOST = "localhost"  # Maps to redis host.
	BROKER_PORT = 6379         # Maps to redis port.
	BROKER_VHOST = "0"         # Maps to database number.
	#this line will screw up things for ghettoq backend
	#CELERY_DEFAULT_EXCHANGE = "tasks" 
	CELERY_IMPORTS = ("tasks", )


Follow this `link`_ for more details

.. _link: http://celeryq.org/docs/configuration.html#redis-backend-settings
