Bug or feature of western union money transfer service
######################################################
:date: 2008-12-09 17:04
:author: Alex
:tags: general

Today, I was trying to transfer money into Russia using my usual account
on westernunion.co.uk. My first attempt clearly failed, because Safari
(recently updated) isn't supported by website.

Second attempt was successful, and results in following page:

|image1|

So, transaction was completed, but in order to complete transfer you
need to communicate MTCN to receiving party.

I looked at the code of the page and it's there:

'''
<<script language="javascript">

RCPcountry = "RU";

</script>
'''

'''
       <script language="javascript"\>MTCN = "*";</script><script language="javascript"\>txnFee = "14.0";</script>

'''
and etc.

But nicely wrapped in javascript tag.

So, my question is it a bug or western union trying to help themselves
in a difficult time? It's too nice bug to have.

.. _|image2|: http://picasaweb.google.com/lh/photo/rIUszCQkbGsfiEqQSyjuLw

.. |image0| image:: http://lh6.ggpht.com/_8_h312mL7b0/ST5wLsTZayI/AAAAAAAAA9I/UrL8WRiw4CI/s144/Picture%202.jpg
.. |image1| image:: http://lh6.ggpht.com/_8_h312mL7b0/ST5wLsTZayI/AAAAAAAAA9I/UrL8WRiw4CI/s144/Picture%202.jpg
.. |image2| image:: http://lh6.ggpht.com/_8_h312mL7b0/ST5wLsTZayI/AAAAAAAAA9I/UrL8WRiw4CI/s144/Picture%202.jpg
