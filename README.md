simbo
=====

An experiment in rethinking A/B testing, based on Sequential Model-Based Optimization (SMBO).

Despite being big believers in A/B testing, there are some flaws that we believe can be done without (note that not all scenarios result in all the issues, but in general there are tradeoffs that need to be made between them):

- Manual intervention: A/B testing is a manual process with scheduling tests and making decisions. Furthermore, these manual steps add human bias to the results.

- Poor scalability to higher dimensional parameter spaces: since the search space grows exponentially in the number of variables to test, practicioners are generally forced into testing a small subset of variables on their own.

- One parameter at a time: A lot of time is just wasted testing parameters that have absolutely no effect.

- Greedy/local search is a poor optimization algorithm: because of the previous point, decisions are often made in a sequential manner, which excludes entire regions of the search space. Even if this may not be that big of an issue in some domains, it could result in a much slower convergence rate compared to other algorithms.

- Ending experiments early: though not part of proper methodology, it happens at times that experiments are stopped early. This leads to many false positives. (Search for "Most Winning A/B test results are Illusory").

- Starting from scratch: experiments don't take past data into account.

Requirements
---

This was tested on:

- Python 2.7.6

- Packages in requirements.txt

- requirements of [python-nvd3](https://github.com/areski/python-nvd3)

Running
---

`python server.py`

Usage
---

1. Start a new experiment, or enter the id of an existing one.
2. Enter the schema for your dataset.
3. Send GET requests to your experiment's sample url to get a set of parameters to use.
4. Send POST requests with the _id of those parameters and the result of your objective function (with key _obj) to the same url.

That's it. The parameters should get better and better over time. Feel free to change the schema at any time (make sure each parameter has a unique name) and look at the visualizations to see the results so far.

How It Works
---

Initially, parameters will just be randomly spread out through the search space. After a bit of initial exploration is completed, we train a model to learn which areas of the search space are most promising. We then sample a very large number of points from the search space, evaluate which of those points would result in the largest expected improvement, and use the top few of those points as future parameters.

As an interesting side effect of this implementation, we can combine personalization and A/B testing into the same step, and optimize the variables that one would A/B test for based on user features.

FAQ
---

#### How well does it work? ####

It seemed to work quite well (see the demo code in /demo). Additionally, the optimization algorithm is incredibly simple and should be very easy to optimize for whatever use case one might have.

#### Quantitatively, how does this compare to A/B testing? ####

We can't tell. A/B testing is by design a manual process (see above regarding scheduling), and it's impossible to fairly compare an automatic process to a manual one.

While simbo is meant to solve the same problem as A/B testing, they solve it in very different ways. In our opinions though, each has its uses. A/B testing would be better in scenarios when domain knowledge could allow for quicker convergence to optimal solutions or statistical significance needs to be known, and tools like simbo would be better when data is scarce/expensive, there is a lack of domain knowledge, a team doesn't want to be burned with manual managing tests, or there is a very large search space.

#### How can simbo handle personalization at the same time? ####

The beauty of using SMBO for this is that we use models to learn which sets of parameters work well together. By treating personalization features (e.g. demographics) as constant parameters of the model, the model will attempt to find the best set of parameters including the constant ones, hence each of the free parameters will be optimized for the given personalization features.

Because the technique is very well suited to high-dimensional problems, adding a few additional parameters won't affect the performance too much.

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

Future Plans
---
1. Use a real database. (The initial prototype was made during a hackathon, hence a little hacked together).
1. Redo the web interface.
1. Add more kinds of distributions for the parameters.
1. Use online models for the SMBO.
1. Allow for personalization.
