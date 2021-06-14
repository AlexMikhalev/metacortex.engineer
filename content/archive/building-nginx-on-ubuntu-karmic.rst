Building nginx on ubuntu karmic
###############################
:date: 2010-02-12 06:33
:author: Alex
:tags: linux, web

Building nginx on ubuntu

sudo aptitude -R install build-essential libpcre3 libpcre3-dev
libpcrecpp0 libssl-dev zlib1g-dev

.. raw:: html

   <p>

::

    ./configure --prefix=/etc/nginx \--sbin-path=/usr/sbin/nginx \--conf-path=/etc/nginx/nginx.conf \--error-log-path=/var/log/nginx/error.log \--pid-path=/var/run/nginx.pid \--lock-path=/var/lock/nginx.lock \--user=www-data \--group=www-data \--http-log-path=/var/log/nginx/access.log \--http-client-body-temp-path=/var/lib/nginx/body \--http-proxy-temp-path=/var/lib/nginx/proxy \--http-fastcgi-temp-path=/var/lib/nginx/fastcgi \--with-cc-opt="-O2 -fno-strict-aliasing" \--with-http_gzip_static_module \--with-http_ssl_module \--with-http_geoip_module

.. raw:: html

   </p>

