Prototyping and testing in scientific programming
#################################################
:date: 2008-12-11 14:19
:author: Alex
:tags: blog, general, science

What we often do in signal processing research is called prototyping.
Commonly used tools for prototyping mathematical model is Matlab and
Simulink, Mathematica and similar “bricks”.

.. raw:: html

   </p>

Prototyping require a lot of thought and easy writing of “throw it away”
code. Once prototype is finished we stick with a tool and keep writing
code, like writing mex file for Matlab, new dll based modules for
labview and keep going until we hit the wall, performance or some other
limitations of the development environment, in which we are working.

Our code gets messy and with every iteration it only gets worse.

.. raw:: html

   </p>

It’s not the only way to go. For years programmers used one tool for
quick prototyping and switched tools for final release. Often you can
predict that you will need to write you own .dll for labview box, so it
may be worth spending some time getting C code right.

.. raw:: html

   </p>

One of the concepts of good programming which helps to improve your own
code is unit testing. I don’t know why, but this topic is considered to
be advanced and you will rarely see it in scientific programming books.

.. raw:: html

   </p>

Unit testing exists even for `matlab`_.

.. raw:: html

   </p>

Writing the tests is a good way to rewrite the pieces of code and still
be sure you didn’t break your model.

I have heard about test driven development before, but I haven’t used it
until now. This year I am writing very complex WiMAX interference model,
with arbitrary number (hundreds) of transmitter and receiver pairs. I
wanted to make sure that my model doesn’t break laws of physics,
especially after my transmitters become directional. So I had to write a
lot of tests. I switched from Matlab to python (writing complex data
structures in Matlab like 5 dimensional hashed hash is not a fun) and I
found it really easy to write a test, then rewrite the code in the model
and making sure model still correct.

From now on, I will try to programme in the following fashion:

.. raw:: html

   </p>

#. Write prototype

#. Write test code for working prototype

#. Rewrite prototype as much as you like, just keep tests up to date

.. raw:: html

   </p>

So far keeping tests updated was most difficult part, especially high
level complex tests. But it makes refactoring (programmers term for
improving code) very easy. Really easy. I am curious about any book or
articles on the subject.

.. raw:: html

   </p>

What is test?
-------------

.. raw:: html

   </p>

Simplest test for example for square root function should check return
values, like

.. raw:: html

   </p>

.. raw:: html

   <p>

::

    test if sqrt 4 return 2test if sqrt -1 return error (nan) or complextest if sqrt 0 return 0

.. raw:: html

   </p>

It is easy to write and makes rewriting easy. More importantly it builds
great confidence in your own code, which can pay off when you will be
questioned about your results.

I wish I used it before, but my excuse “There is no time to write a test
code” just an excuse.

.. raw:: html

   </p>

.. _matlab: http://xtargets.com/cms/Tutorials/Matlab-Programming/MUnit-Matlab-Unit-Testing.html
