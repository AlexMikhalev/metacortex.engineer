Installing duplicity on Mac os X
################################
:date: 2008-08-11 21:44
:author: Alex
:tags: Uncategorized

Today I installed duplicity on my hpc workstation under gentoo linux.
From my mac at home I wanted to check backup, but installing duplicity
on mac is more cumbersome then "emerge duplicity" on gentoo linux.

Thanks to this post `blog`_ I did it fairly quickly.

Main difference for me that I used macports instead of fink so it goes
like this:

port install librsync

tar zxvf GnuPGInterface-0.3.2.tar.gz

cd GnuPGInterface-0.3.2

python setup.py install

Then

tar zxvf duplicity-0.4.12.tar.gz

python setup.py --librsync-dir=/opt/local install

duplicity collection-status scp://alex@\*//home/alex/backup

I received an error that pexpect missing for this backend

so I did

easy\_install pexpect

After that collection-status worked. I have not tried to use it for
backup though.

.. _blog: http://www.claws-and-paws.com/node/1266
