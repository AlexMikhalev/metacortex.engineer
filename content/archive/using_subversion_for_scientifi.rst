Using subversion for scientific project
#######################################
:date: 2008-07-26 15:10
:author: Alex
:tags: Uncategorized

I used to use version control software long time ago, when I was
web-programmer.

When I started to write matlab code, I wrote a small function which
would save results - usually figures, results of calculations, in a
matlab fig file. Then "Gosh. Was it much better results that were
overwritten a second ago?"

So, in my save\_figure a timestamp appeared:

filename=strcat('fig/',figure\_name,regexprep(num2str(now), '\\.', ''));

I have all results, good and bad time stamped for a last three years.
Happy now?

Not yet, recently I have been asked a lot of questions about the
parameters of the model, and although I wrote down most of them, I
failed to retrieve the files which correspond to the particular set of
results. If you think that half of the figures require two or three days
to repeat one plot, you will understand my feeling as I have a good
number of them.

Solution: Before leaving my last job and changing a carrier from system
administrator to researcher, I installed svn + trac server for my fellow
developers.

Although I was the only person for using trac for keeping track of IT
related issues, developers seems to be happy using svn, rather then cvs
or ms source safe.

I created a local subversion repository, added my thesis first, so I can
keep all versions and reviews my prof was giving me. Sounds good? It
will get better.

There are a lot of tools available for managing svn under linux and mac
os. I use a handy set finder scripts as well as textmate subversion
bundle.

Under linux, kompare and ksvn provide a flawless integration with file
manager (konqueror), so once you feed you svn repository url your will
be pleasantly surprised with a level of control offered by this simple
set. I was.

What's next? Matlab integration: There is no support in matlab off the
shelf, however you will find a modified custom script
http://www.mathworks.com/matlabcentral/files/11596/customverctrl.m which
works fine under linux and mac.

This will give only two commands - check in and check out for matlab
script in the editor, but it's enough for me.

Now, I wanted to have a personal repository. I suggest to speak with
your university IT team, so they can install it inside university
network. It might be possible that they already have it, but you
happened to oversee it.

If they don't have it, there is an alternative:

https://opensvn.csie.org/ and http://www.assembla.com provide a free svn
repository. I am currently using assembla, although I am a bit concerned
about privacy and security.

What do you do for keeping versions of the files on track?

To be continued...
