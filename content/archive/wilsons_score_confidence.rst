Wilson Score Confidence interval
################################
:date: 2013-11-03
:author: Alex
:tags: science, python, julia

Not sure where I got this snipplet - most likely from reddit code or discussion.  

.. code:: python

	from math import sqrt

	def confidence_fixed(ups, downs):
	    if ups == 0:
	        return -downs
	    n = ups + downs
	    z = 1.64485 #1.0 = 85%, 1.6 = 95%
	    phat = float(ups) / n
	    return (phat+z*z/(2*n)-z*sqrt((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n)	


Like for like in Julia

.. code:: julia

	 function confidence_fixed(ups,downs)
	       if ups==0
	          return -downs
	       end
	       n = ups + downs
	       z = 1.64485 #1.0 = 85%, 1.6 = 95%
	       phat = float(ups)/n
		   return (phat+z*z/(2*n)-z*sqrt((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n)
	  end