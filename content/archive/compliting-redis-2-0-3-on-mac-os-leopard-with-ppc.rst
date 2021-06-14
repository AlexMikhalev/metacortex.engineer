Compliting redis 2.0.3 on mac os leopard with ppc
#################################################
:date: 2010-10-28 10:55
:author: Alex
:tags: cloud

Just notes to myself:

redis.c line 10897

.. raw:: html

   <p>

::

      #if defined(__FreeBSD__)    return (void*) uc->uc_mcontext.mc_eip;#elif defined(__dietlibc__)    return (void*) uc->uc_mcontext.eip;#elif defined(__APPLE__) && !defined(MAC_OS_X_VERSION_10_6)  #if __x86_64__    return (void*) uc->uc_mcontext->__ss.__rip; #elif defined (__i386__)      return (void*) uc->uc_mcontext->__ss.__eip;  #else    return (void*) uc->uc_mcontext->__ss.__srr0;  #endif

.. raw:: html

   </p>

.. raw:: html

   <p>

::

      CFLAGS='-mmacosx-version-min=10.5 -arch ppc -sysroot=/Developer/SDKs/MacOSX10.5.sdk' make

.. raw:: html

   </p>

See
[ticket]("http://code.google.com/p/redis/issues/detail?id=119&can=1&q=ppc")
for more details
