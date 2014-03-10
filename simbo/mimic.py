### MIMIC
# Based on:
# Mutual-Information-Maximizing Input Clustering
# De Bonet, Jeremy S., Ch L. Isbell, and Paul Viola.
# "MIMIC: Finding optima by estimating probability densities."
# Advances in neural information processing systems (1997): 424-430.
import numpy as np
from sklearn.mixture import GMM
from sklearn.neighbors import KernelDensity

from optimize_utils import *
from generative_models import MIDependencyTree


def _minimize_mimic(
        fun,
        x0,  # only used to get number of features
        args=(),
        callback=None,
        sampler=None,
        initial_distribution=None,
        domain="gaussian",
        n_iter=10,
        starting_percentile=0.5,
        batch_size=100,  # number of trials for each percentile
        maxiter=None):
    if maxiter is not None:
        batch_size = int(maxiter / n_iter)

    if sampler is None or sampler == "gmm":
        sampler = GMM()
    elif sampler == "kde":
        sampler = KernelDensity()
    elif sampler == "dependencytree":
        sampler = MIDependencyTree(GMM())

    if initial_distribution is None:
        init_size = (batch_size, len(x0))
        if domain is None:
            # assume that the sampler is already fit to sample from
            initial_distribution = sampler.sample(batch_size)
        elif domain == "gaussian":
            initial_distribution = np.random.randn(**init_size)
        elif domain == "binary":
            initial_distribution = np.random.randint(2, size=init_size)
        else:
            raise ValueError("Improper domain: %s" % domain)

    population = initial_distribution

    for percentile in np.linspace(starting_percentile, 0, n_iter):
        # fit previous population
        sampler.fit(population)
        # generate `sample_size` more
        population = sampler.sample(batch_size)
        # compute obj value
        scores = score_multi(fun, population, args, callback)
        # select `percentile` bottom (since we are minimizing)

        cutoff = np.percentile(scores, percentile * 100)
        idx = scores <= cutoff
        # repeat
        population = population[idx]
    x = population[0]
    fval = scores[idx[0]]
    nfev = batch_size * n_iter
    return to_result(x=x, fun=fval, niter=n_iter, nfev=nfev)
