Speeding up cakephp with nginx and no mod_rewrite issues
########################################################
:date: 2010-12-13 17:21
:author: Alex
:tags: blog, web

I am trying to speedup rather crappy php, website build on top of
cakephp and decided to follow this `tutorial`_, I was seriously annoyed
that I can't get rig of /app/webroot prefix in css/js links. I didn't
want to hack them directly because I am using automatic css/js
compression.

It wasn't until I found this `solution`_ from the `ticket`_ closed in
January I managed to fix it.

Quite surprised that in order to dispatch cakephp app I need to patch
the core and there are hundred of unanswered questions/issues about
deployment of cakephp without mod\_rewrite.

PS. Good start - this is my first day of holiday gone.

.. _tutorial: http://andy-gale.com/cakephp-view-memcache.html
.. _solution: https://github.com/cakephp/cakephp1x/commit/2d81d25f410ec9c2527fab92c769e72e04134a0e
.. _ticket: http://cakephp.lighthouseapp.com/projects/42648/tickets/259
