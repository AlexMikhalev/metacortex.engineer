DIY Amazon EC2 Spot Instances price chart
#########################################
:date: 2009-12-17 02:16
:author: Alex
:tags: blog, cloud, general, web

This is a short example how to build very simple chart for EC2 Spot
Instances using `Timeplot`_

Following `Eric Hammond example`_

We are going to plot ec2 c1.medium prices against c1.medium in
eu-west-1, to see how more expensive amazon ec2 instances in Europe

.. raw:: html

   </p>

#. Grab EC2 spot instance price:

   .. raw:: html

      </p>

   ec2-describe-spot-price-history -t c1.medium -d Linux/UNIX \|

   perl -ane 'print "$F[2],$F[1]\\n"'>>data\_ec2.txt

#. Add --region eu-west-1 to the command above so:

    ec2-describe-spot-price-history --region eu-west-1 -t c1.medium -d
    Linux/UNIX \|

    .. raw:: html

       </p>

    .. raw:: html

       <p>

    perl -ane 'print "$F[2],$F[1]\\n"'>>data\_ec2\_eu.txt

3. You also need to use two files `time-plot.js`_ and `html file`_
4. Save them in one directory (or use correct file paths)
5. That's it, folks. It should look like `this`_.

.. raw:: html

   </p>

.. _Timeplot: http://www.simile-widgets.org/timeplot
.. _Eric Hammond example: http://alestic.com/2009/12/ec2-spot-instance-prices
.. _time-plot.js: http://media.sci-blog.com.s3.amazonaws.com/wp-content/uploads/2010/09/time-plot.js
.. _html file: http://media.sci-blog.com.s3.amazonaws.com/wp-content/uploads/2010/09/ec2_plotter.html
.. _this: http://media.sci-blog.com.s3.amazonaws.com/wp-content/uploads/2010/09/ec2_plotter.html
