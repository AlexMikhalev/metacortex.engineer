Estimating user lifetimes with PyMC - Corrected code
#####################################################
:date: 2013-08-27 
:author: Alex
:tags: cloud, science 

I was trying to follow this `post`_, but github gists miss few variables, correct code shall be:

.. code:: python

	import pymc as mc
	import numpy as np

	N=20

	#create some artificial data, like the data in the figure above. 
	lifetime = mc.rweibull( 2, 5, size = N ) 
	birth = mc.runiform(0, 10, N)
	 
	censor = (birth + lifetime) > 10 #an individual is right-censored if this is True 
	lifetime_ = np.ma.masked_array( lifetime, censor ) #create the censorship event. 
	lifetime_.set_fill_value( 10 ) #good for computations later.
	 
	#this begins the model 
	alpha = mc.Uniform("alpha", 0,20) 
	#lets just use uninformative priors 
	beta = mc.Uniform("beta", 0,20) 
	obs = mc.Weibull( 'obs', alpha, beta, value = lifetime_, observed = True )




Posteriory 


.. code:: python

	@mc.potential
	def censorfactor(obs=obs): 
	    if np.any((obs + birth < 10)[lifetime_.mask] ): 
	        return -100000
	    else:
	        return 0
	 
	#perform Markov Chain Monte Carlo - see chapter 3 of BMH
	mcmc = mc.MCMC([alpha, beta, obs, censorfactor ] )
	mcmc.sample(50000, 30000)



.. code:: python 

	N = 2500 #125 times more data than before
	lifetime = mc.rweibull( 2, 5, size = N )
	birth = mc.runiform(0, 10, N)
	censor = ((birth + lifetime) >= 10) #an individual is right-censored if this is True 
	lifetime_ = lifetime.copy()
	lifetime_[censor] = 10 - birth[censor] #we only see this part of their lives.
	 
	 
	alpha = mc.Uniform('alpha', 0, 20) #lets just use uninformative priors again
	beta = mc.Uniform('beta', 0, 20)
	 
	@mc.observed
	def survival(value=lifetime_, alpha = alpha, beta = beta ):
	    return sum( (1-censor)*(log( alpha/beta) + (alpha-1)*log(value/beta)) - (value/beta)*(alpha) )
	 
	mcmc = mc.MCMC([alpha, beta, survival])
	mcmc.sample(50000, 30000)




.. _post: http://blog.yhathq.com/posts/estimating-user-lifetimes-with-pymc.html