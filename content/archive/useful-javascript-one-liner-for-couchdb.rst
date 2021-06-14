Useful JavaScript one-liner for couchdb
########################################
:date: 2011-06-01 16:35
:author: Alex
:tags: cloud, web

I found myself using more and more of this one-liner for working with
couchdb database:

.. raw:: html

   <p>

::

     var getNewDatabusUUID = JSON.parse($.ajax({ type: "GET", url: "/_uuids/",                async: false }).responseText);  $.log("New uuid generated " + getNewDatabusUUID.uuids);

.. raw:: html

   </p>

this example retrieves new uuids from couchdb, but I was using it to
retrieve \_rev of the document before deletion and similar one-off
problems.
