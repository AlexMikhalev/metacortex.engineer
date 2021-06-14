---
title: Acoustic Source Localization using Hough Transform
date: 2015-12-26
author: Alex
tags: [julia, Machine Learning, hough transform, sound, source localization]
---
This is rather ugly solution out of conversation with MFTI students. Warm up for "Programming Kata".

Scene: cheap hardwire assempled into robot with 3 mics separated 10 cm each. On "Clap" robot is running towards clapper.

Simulation:

.. code:: julia

	# Scene

	c_speed_m = 340.29 # m / s
	c_speed_cm= 34029 # cm/sec

	# Grid size - area of interest, my assumption our mics would not pickup sound of clap (chirp) further than 10 m.

	x_max = 1000 # cm
	y_max = 1000 # cm

	# Target position

	x_t = 751
	y_t = 657


	# Sensor position

	x1 = 035
	y1 = 036

	x2 = 045
	y2 = 036

	x3 = 035
	y3 = 026

	sigma_time=7.4E-9
	# this is not correct value for this system - 7.4E-7 is GPS timing error synchronisation, assuming all mics connected by wire


	real_distance1=sqrt((x_t-x1)^2+(y_t-y1)^2)
	real_distance2=sqrt((x_t-x2)^2+(y_t-y2)^2)
	real_distance3=sqrt((x_t-x3)^2+(y_t-y3)^2)


	# time_2=real_distance2*10^3/c+(sigma_time*rand);
	# TIME of Arrival

	time_2=real_distance2/c_speed_cm;
	time_1=real_distance1/c_speed_cm;
	time_3=real_distance3/c_speed_cm;

	TDOA1 = time_2 - time_1 + (sigma_time*randn()); # sensor 1 is a reference
	TDOA2 = time_3 - time_1 + (sigma_time*randn());
	TDOA3 = time_3 - time_2 + (sigma_time*randn());
	TDOA4 = time_2 - time_3 + (sigma_time*randn());


TDOA can be obtained using ROOT-MUSIC or cross-correlation techniques. In the past I saw XOR based TDOA estimator.

Applying Hough Transform approach (non linear, non-parametric etc estimator) with principle "throw everything on the wall, see what sticks", very bruteforce, not julia-like example, but very robust algorithm.


.. code:: julia

   A_tdoa=zeros(x_max,y_max);

   sigma_range=c_speed_cm*sigma_time/(sqrt(2))

   tic();
   for x = 1:x_max
       for y = 1:y_max

           sigma_range=c_speed_cm*sigma_time/(sqrt(2));
                  r2=sqrt((x-x2)^2+(y-y2)^2);
                  r1=sqrt((x-x1)^2+(y-y1)^2);
                  delta_r=(r2-r1);
                  p=(delta_r)-(c_speed_cm*TDOA1);
                  l=exp(-0.5*p^2/sigma_range^2)/2;
                  A_tdoa[x,y]=A_tdoa[x,y]+(l);

           #         very ugly second tdoa measurement TDOA2
                  r3=sqrt((x-x3)^2+(y-y3)^2);
                  r1=sqrt((x-x1)^2+(y-y1)^2);
                  delta_r=(r3-r1);
                  p=(delta_r)-(c_speed_cm*TDOA2);
                  l=exp(-0.5*p^2/sigma_range^2)/2;
                  A_tdoa[x,y]=A_tdoa[x,y]+(l);

        #         very ugly third tdoa measurement TDOA3
                  r3=sqrt((x-x3)^2+(y-y3)^2);
                  r2=sqrt((x-x2)^2+(y-y2)^2);
                  delta_r=(r3-r2);
                  p=(delta_r)-(c_speed_cm*TDOA3);
                  l=exp(-0.5*p^2/sigma_range^2)/2;
                  A_tdoa[x,y]=A_tdoa[x,y]+(l);

                  r3=sqrt((x-x3)^2+(y-y3)^2);
                  r2=sqrt((x-x2)^2+(y-y2)^2);
                  delta_r=(r2-r3);
                  p=(delta_r)-(c_speed_cm*TDOA4);
                  l=exp(-0.5*p^2/sigma_range^2)/2;
                  A_tdoa[x,y]=A_tdoa[x,y]+(l);

       end
   end
   toc();

   using PyPlot;

   imshow(A_tdoa)

   maxp_value = maximum(A_tdoa,1)

   (value,y_est)= findmax(maxp_value)

   maxp_value_x = maximum(A_tdoa,2)

   (value_x,x_est)= findmax(maxp_value_x)

   rmse=sqrt((x_t-x_est)^2+(y_t-y_est)^2)


Out of one measurement I manage to get fairly good results - 30 cm, super precision!

Feel free to use or ask questions, I applied some "heuristic" - sqrt(2) in equation should be something like `sqrt(1-cos(sqrt(angle between sensor and point on hyperbolae)))`
