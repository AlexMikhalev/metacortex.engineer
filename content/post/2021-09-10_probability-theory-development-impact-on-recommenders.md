---
title: "The probability theory development impact on recommenders"
author: "Alex Mikhalev"
date: 2021-09-10T13:36:32.223Z
lastmod: 2021-09-29T18:29:24+01:00

description: ""

subtitle: ""




aliases:
- "/the-probability-theory-development-impact-on-recommenders-60848fbb984c"

---

You got probability and likelihood calculation wrong; this is why you can’t build a proper recommender.

I finally finished reading long overdue essay (300 лет в искаженной реальности) in Russian, which is referencing Nature publication “[The ergodicity problem in economics](https://www.nature.com/articles/s41567-019-0732-0)” and “[Time to move beyond average thinking](https://www.nature.com/articles/s41567-019-0758-3)”.

Those pieces are critical to understanding if you want to build a practically useful intelligent system today. The implications of this development are exposing how economists and risk managers treat probability can be seen in GDP or performance of pension funds. Still, the one example which is easier to relate is the Amazon recommender system: the reason why you keep seeing the recommended product even after you bought it, because time is not part of the calculation. See the [history of the Amazon recommendation algorithm, ](https://www.amazon.science/the-history-of-amazons-recommendation-algorithm)but the most important point — the time is not the part of the calculation conceptually. Hence you have a less useful user experience as you might have if likelihood would be calculated as physicists do.

I came across this challenge with likelihood calculations and time during data fusion work at Cranfield University, and I have a pretty long mathematical chapter trying to address it: the impact of time is visible in data fusion /measurements fusion, including famous papers on geolocation using Extended Kalman Filter — if your first guess not in the vicinity of the target, then EKF can’t converge, because you got your model wrong. The difference is that time in real-world sensor problems is extremely important, and that’s why heuristic-based algorithms, like Hough transform, Evolutionary algorithms or even Deep Learning NN perform better than pure Bayesian-based estimators.

Most of the processes in real life a non-ergodic — see Nassim Taleb’s work, and treating them as ergodic leads to disastrous results. We shall start building intelligent systems based on the correct approach to avoid the risks of Machine Learning based products.

Are you interested in the maths heavy chapter on bayesian vs heuristics and how it connects to causal inference (the answer to everything is 48, not 42)? Let me know in thumb apps or comments.

* * *
Written on September 10, 2021 by Alex Mikhalev.

Originally published on [Medium](https://medium.com/@alexmikhalev/the-probability-theory-development-impact-on-recommenders-60848fbb984c)
