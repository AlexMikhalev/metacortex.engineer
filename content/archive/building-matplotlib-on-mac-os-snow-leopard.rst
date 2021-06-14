Building matplotlib on Mac OS snow leopard
##########################################
:date: 2010-11-19 14:21
:author: Alex
:tags: general, science

I spent a lot of time trying to figure out how to build matplotlib on
Snow Leopard without using macports - I prefer to use homebrew instead
and ended up with incompatible binaries, until I found
['This'](http://blog.hyperjeff.net/?p=160 "this post"). Notes

Edit make.osx

.. raw:: html

   <p>

::

        MACOSX_DEPLOYMENT_TARGET=10.6PREFIX=/usr/local## You shouldn't need to configure past this point (and yet…)PKG_CONFIG_PATH="${PREFIX}/lib/pkgconfig"CFLAGS="-arch i386 -arch x86_64 -I${PREFIX}/include -I${PREFIX}/include/freetype2 -isysroot /Developer/SDKs/MacOSX10.6.sdk"LDFLAGS="-arch i386 -arch x86_64 -L${PREFIX}/lib -syslibroot,/Developer/SDKs/MacOSX10.6.sdk"FFLAGS="-arch i386 -arch x86_64"

.. raw:: html

   </p>

Set

.. raw:: html

   <p>

::

    wxagg = False

.. raw:: html

   </p>

in setup.cfg

And finally:

.. raw:: html

   <p>

::

    sudo make -f make.osx fetch deps mpl_build mpl_installsudo python setup.py install

.. raw:: html

   </p>

