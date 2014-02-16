simbo
=====

An experiment in rethinking A/B testing, based on Sequential Model-Based Optimization (SMBO).

Requirements
---

Python

- Python 2.7.6

- Packages in requirements.txt

- requirements of [python-nvd3](https://github.com/areski/python-nvd3)

Running
---

`python server.py`

How It Works
---

TODO

FAQ
---

#### How do you calculate the best points to use? ####

We compute each points' expected positive improvement (see page 8 of [this paper](http://www.cs.ubc.ca/~hutter/papers/11-LION5-SMAC.pdf)). To quote the paper:

> it offers an automatic tradeoff between exploitation (focusing on known good parts of the space) and exploration (gathering more information in unknown parts of the space)

#### What about multiple objective values? ####

While it would be possible to model/optimize for multiple objective values, we believe that is is unnecessary. When it comes to making a decision, each of the multiple objectives will have to be combined together to rank the choices, hence that combination having to occur either way. We just require it to happen explicitly.

#### How can random search possibly be better than A/B testing? ####

![Random Search Image](images/random_search.png)

A common complaint in our experience and those we have spoken to is that a majority of parameters tested are unimportant. By testing multiple parameters at the same time, one can explore the possible options for the important variables much more quickly.

Imagine there are 99999 useless parameters to test, and one good one. A grid search (A/B test) would have search through each parameter individually, while random search can search through values of the good parameter with every experiment.

For more information on the merits of random search, see [this paper](http://jmlr.org/papers/volume13/bergstra12a/bergstra12a.pdf).

#### Why not just use random search then? ####

Because we can do better! Random search can be very dumb when it comes to searching through parameter space, since it doesn't take into account any history. By taking historic results into account, we can guide the search areas with known good behavior (to search more thoroughly and try to improve on our best) or areas that are poorly explored (since we have little to no information on how good those parameters would behave).
