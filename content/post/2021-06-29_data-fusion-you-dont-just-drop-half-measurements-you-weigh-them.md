---
title: "Data fusion: you don’t just drop half measurements you weigh them"
author: "Alex Mikhalev"
date: 2021-06-29T15:25:51.640Z
lastmod: 2021-09-29T18:29:15+01:00

description: ""

subtitle: ""




aliases:
- "/data-fusion-you-dont-just-drop-half-measurements-you-weigh-them-c0fbd6a60027"

---

Update: very simple example of working data fusion in every phone: panorama photos. Stitching images is a hard image-processing problem, adding gyro measurements made it way simpler.

Newsletter from Comet-ML arrived in my mailbox and it nearly forced me to spill coffee, the passage which caught my eyes:

[**From CVPR 2021: Tesla’s Andrej Karpathy on a Vision-Based Approach to Autonomous Vehicles**](https://www.youtube.com/watch?v=g6bOwQdCJrc&list=PLvXze1V52Yy2OY67mz2Jy-JcnEw8GUZEl&index=11&utm_campaign=Monthly%20newsletter&utm_source=hs_email&utm_medium=email&utm_content=136820874&_hsenc=p2ANqtz-_77kjQ26nVBwSMN5ryfLcLh1OElbw-VSukWSRV3EVQHIhmNFmp-4tJ8tBVioVoI6FStxcT7MCHwRxO7vduGez-3xA55Q)

Tesla is doubling down on its vision-first approach to self-driving cars and will stop using radar sensors altogether in future releases.

From its inception, Tesla has taken a different approach to most other companies developing a self-driving car that doesn’t rely on Lidar. Instead, they used a combination of radar sensors and 8 cameras placed around the vehicle.

In this talk at CVPR 2021, Andrej Karpathy explains the challenges with this approach and [why Tesla has decided to focus on cameras](https://is.t.hubspotemail.net/e2t/tc/VWrRkc108hLtW4D-SMR6HsJL9V7Wb0N4tp8mZN11fKVG5nxG7V3Zsc37CgSzWW2czlc066WKnMW4P97pL3hnWzqW2vFyD9240GyFVXq8Nh8zrmXjW1Cj0-w1Jkv2jN70bqcydk4bzVRLjhS7086yjW5LY67q1XBqvcN4S8fBXp5-9TW6RNmMF3MZGkkW7mp7BM7bK4GYW933gHR3HpBnyW1wvT1v93G12tW1-p5cv6_HlFSW9lGLm27R8rqFW6198lq2ZSv5gW4ghzsp3Xc4DYW8CtYw13NGcqvVytCcG612Sq0Vsxqqy4-JNtkW8NLwj93W6q4mW1cwqlP1R2MKHM297JnmSl12W6HCs445g6KqLW4fF6GG58JKgdW107bF57QHGq2W5_-rCW1j0FR3W8xwwCG8Jg6m0W1bfCYB4vZRCYW95wv9696Ts1PW1B2tgR7m3Nq5W2ds6Bl7LyNpm3mfk1) and stop using radar sensors. The main challenge with using different sensor types is sensor fusion. [As Elon Musk puts it:](https://is.t.hubspotemail.net/e2t/tc/VWrRkc108hLtW4D-SMR6HsJL9V7Wb0N4tp8mZN11fKX73p_9rV1-WJV7CgFdGW2SvmfG6njMVCN4jBJcJk-pQJW7TBM_Q7-vqRmN7HFdMRdgnTRW98z2s28P98pXW6GtTpb7tj_yGVLqCT7660B1zW5J3rSV10YFfBW8Pm0md6Cl4B4W3WL5N48wscC9W3RJ0p87DlSVmW27fc4b8QrlgSW5wCQDZ2LdT9-W5nd2qR12CXNMW6n5jt11SfrwqW2Mylyl4ZZp6mN3yHmR8sHDRGW4MZp3w9dhRb5W1QBqBJ2G5W97N3Xn0x3gy3vDW89RHvR8LTqh-W2mK-zb7vr8LgW689Btc3dY5dpW3ZHxJ5909QvNW5KRftb2FDCpDW5NqTDp3Wtlh235vY1) “When radar and vision disagree, which one do you believe? Vision has much more precision, so better to double down on vision than do sensor fusion.”

If you have sensor data, from real-world sensors you don’t just discard half of them because others are more precise: consider a scenario on which I worked for several years: flying sensor platform at speed x Mach (or at 30–60 meters per second, but multiple of those) receive a radio signal and the one which is x Mach survives for 15 seconds after that and 30–60 meter platform about a minute or two minutes at max.

You can get very precise measurements using “range-based” techniques, like time of arrival or time difference of arrival, except while they provide high resolution they give you at least two points of intersection ( you need 3 sensors or two platforms to resolve ambiguity) and angle of arrival measurements, which are so “precise” that due to fading you will be lucky to get right quadrant, there is also frequency difference of arrival (but I know you already bored).

The area which studies it for the last 80 years is ELINT, read up Steve Blanks [write up what fun it was](https://steveblank.com/2009/04/13/story-behind-the-secret-history-part-iv-undisclosed-location-library-hours/). Data fusion will result in decision aeroplane choosing attack or manoeuvre out of the range of missiles, make it wrong and you are down. And no, you can’t take more measurements — deal with the ones you have or be at risk of exposure and being shot down.

To comment on the above marketing hype: Neural Networks are bad for data fusion to start with, there are a number of algorithms developed specifically for that problem — bootstrap filter, particle filter, evolutionary algorithms or my [own stuff](https://www.academia.edu/7525934/Multi_Cluster_Agent_Based_Emitter_Geolocation_using_Hough_Transform_Data_Fusion) based on Hough Transform. NN will not learn the physics and limitations of radar measurements compared to cameras, but human engineers designed that systems do, we can incorporate human knowledge into the system by assigning appropriate weights to different types of measurements.

There is a wider philosophical piece on Bayesian vs non-Bayesian — parametric estimations for data fusion, but it will need a lot of maths to support discussion and will be published in my blog at [www.sci-blog.com](https://www.sci-blog.com/)

* * *
Written on June 29, 2021 by Alex Mikhalev.

Originally published on [Medium](https://medium.com/@alexmikhalev/data-fusion-you-dont-just-drop-half-measurements-you-weigh-them-c0fbd6a60027)
