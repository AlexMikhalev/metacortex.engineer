Mysql DB and unicode utf8
#########################
:date: 2009-12-25 00:25
:author: Alex
:tags: linux, web

Do you expect newest Ubuntu server 9.10 (karmic) to support utf8 in
mysql server out of the box? Well, it doesn't.

Don't forget to put small file \*/etc/mysql/conf.d/charset.cnf\*:

[mysqld]

character-set-server=utf8

default-collation=utf8\_unicode\_ci

character\_set\_client=utf8

[mysql]

default-character-set=utf8
