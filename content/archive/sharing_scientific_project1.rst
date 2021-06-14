Sharing scientific project: the way to the bright future
########################################################
:date: 2008-11-30 22:26
:author: Alex
:tags: blog, general, science

I recently had a chat with people who will be doing "portal" for our
university, for sharing information between departments, may be even
between groups of the researchers. Nice guys will be using ms sharepoint
as back-end

.. raw:: html

   </p>

I hope they know what they are doing, otherwise it will be yet another
useless portal with ridiculous development time. But I decided to put my
thoughts together on this subject, while they are fairly fresh. Let's
look at the requirements for sharing research project:

\* Equation support. People who tells about equation editor in MS Word,
unlikely had to use it often. So for now, let's say we need Latex or
MathML. I bet for chemistry scientists there is their own form of
writing equations, so it should be plugin based.

.. raw:: html

   </p>

-  Bibliography, something bibtex compatible similar to
   http://www.citeulike.org/, but project oriented. Since most of the
   databases support REST/XML type api integration with PubMEd and IEEE
   should be fairly straight forward.

-  Version control on any stage similar to mercurial/git. For separate
   pages and bibliography. Github or trac can be used as a way to start.

-  Distributed and decentralised. That's a dream. It would be cool to be
   able to synchronise offline and online activity. Again as it is done
   in mercurial/git distributed version control systems (DVCS).
   Actually, it should be doable, for example, if whole database kept in
   DVCS, it should be possible to synchronise the data from offline into
   online, with collision detection and automatic resolution.

-  For security obsessed gpg based encryption on low level. Difficult
   and probably will screw version control.

.. raw:: html

   </p>

I hacked Latex plugin for movable type and I can add graphviz plugin for
mt as well, but I don't think MT will be suitable platform to start
this. Although community edition looks attractive.

So, does anyone knows customizable wiki based on python and storing data
in mercurial?

If not, anyone for the challenge of hacking it all together? This year I
am writing things in python, due to google apps engine and my own third
attempt to grab it. And it didn't finish with smashed keyboard so far,
so links to python project preferable.

.. raw:: html

   </p>

