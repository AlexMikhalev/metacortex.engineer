Change of database: Percona Mysql to Postrgres for django
#########################################################
:date: 2011-10-15 20:36
:author: Alex
:tags: cloud

Colleague of mine came with strange bug:

1. I am opening python shell, and sending request User.objects.all()

It returns valid information

\* then i'm adding user via web site

\* then i send request User.objects.all() again and new user is missing.
If i will reopen shell then everything will be ok

2. When i'm running "python manage.py test name\_of\_application"
creating and deleting database takes too long

Percona Server version: 5.5.15-55 Percona Server (GPL), Release 21.0

We decided that Postgres will be better and switched to it
