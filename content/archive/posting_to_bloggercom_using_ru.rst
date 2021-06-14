Posting to blogger.com using ruby GData
#######################################
:date: 2008-08-11 22:46
:author: Alex
:tags: Uncategorized

I would like to be able to cross-post from textmate or from movable type
to blogger.com.

Unfortunately I didn't find any working scrips on perl. To be fair I
found one and another has been emailed to me. But I found ruby-gdata
library and wanted to play with it.

As usual gem can be installed gem install GData, but

bloggerpost script would not work straight away.

export GDATA\_PASS=

export GDATA\_USER=alex@

./bloggerpost blog\_id

and this will fail.

You need to look at the patch `here`_

and apply it to ../lib/gdata/blogger.rb before it will work.

Next step to check blogger.rb from textmate blogging bundle.

.. _here: https://rubyforge.org/tracker/index.php?func=detail&aid=18321&group_id=3077&atid=11849
