Django optimisation in production
#################################
:date: 2011-07-10 20:08
:author: Alex
:tags: cloud, python, web

Few days ago I realised that my django installation in production
started producing too many memory errors - thanks to monit memory alerts
were filling my mailbox without any serious service interruption. But
hundreds email messages daily annoyed me enough to look deeper into
trouble.

1) I switched on django debug true, noticed a large delay on SQL
request. Also enabled in my.cnf slow-log part with number 5.

Solution one: Added db\_index=True to the model.py to the fields used in
where clauses. Indexes which I created with help of ./manage sqlindexes
didn't work, so I had to login into dbshell and perform EXPLAIN and
CREATE INDEX manually.

2) Added distinct() to most of my queries - I didn't bother to filter
duplicate queries, because values() was doing it for me.

3) Added db.reset\_queries() to the top of my view.py, because I deploy
django via fcgi with nginx frontend, django was tracking queries for a
"session" which is never ended.

4) I didn't notice any significant performance improvement until I
decided to create a cache of sql requests, put /manage.py
createcachetable my\_cache\_table and then went to settings.py.

OMG:

.. raw:: html

   <p>

::

    CACHE_BACKEND = "locmem:///?max_entries=3000"

.. raw:: html

   </p>

which is the worst cache settings you can have for django in production.

changing it to

.. raw:: html

   <p>

::

     CACHE_BACKEND = "db://my_cache_table"

.. raw:: html

   </p>

produced serious performance improvement. (Yes, I can put memcached or
redis if I need it, but I don't think I need it at the moment - my
traffic is google bot.)
