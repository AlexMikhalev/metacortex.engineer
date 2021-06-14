Speeding up javascript: listing of elements from couchdb using jQuery mobile
############################################################################
:date: 2011-05-15 19:39
:author: Alex
:tags: web

As I mentioned in my `previous post`_\ I was using `this tutorial`_ as a
basic for CRUD application for couchdb.

But I found that listing of "albums" is very slow. I modified code using
for loop examples from the book "High Performance Javascript" and
results of the JS `tests from gaperton livejournal`_.

A lot of words for three line change:

.. raw:: html

   <p>

::

     function refreshAlbums()      {*          $("#albums").empty();         $db.view("albums/albums",{            success: function( data ) {                      var listItem;                    var header;                    var albumLink;                    data.rows.reverse();           for ( var i=data.rows.length;i--;)                    {                album = data.rows[i].value;                artist = album.artist;                title = album.title;                description = album.description;                listItem =listItem+  "" +                            "" + artist + "<\/h2>" +                            "" + title + "<\/p>" +                            "" + description + "<\/p>";                                            }             $("#albums").html( listItem );                     $("#albums").listview( "refresh" );                    $.fixedToolbars.show();                }            });      }      $(document).ready( handleDocumentReady );

.. raw:: html

   </p>

Also, if you update jquery.mobile to jquery.mobile-1.0a4.1, path in
scripts in template/partials should look like:

.. raw:: html

   <p>

::



.. raw:: html

   </p>

.. _previous post: http://sci-blog.com/2011/04/checkbox-and-select-elements-in-couch-db/#more-196
.. _this tutorial: http://custardbelly.com/blog/?p=244
.. _tests from gaperton livejournal: http://gaperton.livejournal.com/55094.html
