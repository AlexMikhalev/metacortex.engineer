Nginx and Movable Type (Pro)
############################
:date: 2009-08-15 05:35
:author: Alex
:tags: blog, web

For those who would like to play heroes and who are trying to run
Movable Type under nginx in cgi mode, additional fastcgi parameters in
nginx:
'''
fastcgi\_param    PERL5LIB $document\_root/mt/lib;
   fastcgi\_param    MT\_HOME $document\_root/mt;
   fastcgi\_param    MT\_CONFIG $document\_root/mt/mt-config.cgi;
'''

the rest can be taken from `here`_ with cgi wrapper.
With this additional parameters mt-check will be successful, but in my
case it failed with:

'''Can't connect to data source '' because I can't work out what driver to use (it doesn't seem to contain a 'dbi:driver:' prefix and the DBI_DRIVER env var is not set) at /var/www/*/htdocs/mt/extlib/Data/ObjectDriver/Driver/DBI.pm line 75 at /var/www/*/htdocs/mt/extlib/Data/ObjectDriver/Driver/BaseCache.pm line 320 '''

Since I don't know whom to blame for this error and can't fix it on
spot, I will leave MT under apache for now.

For those interested in runing MT under lighttpd, this `tutorial`_ makes
much more sense, then official doc, and it's closer to my previous blog
install.

.. _here: http://nginx.localdomain.pl/wiki/FcgiWrap
.. _tutorial: http://blog.tapirtype.com/2006/12/mt33_lighty_fastcgi/
