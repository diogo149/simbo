"""
Based on:
Mutual-Information-Maximizing Input Clustering
De Bonet, Jeremy S., Ch L. Isbell, and Paul Viola. "MIMIC: Finding optima by estimating probability densities." Advances in neural information processing systems (1997): 424-430.
"""
import numpy as np
from generate import *
from sklearn import mixture
from scipy.optimize import minimize


def mimic_optimizer(
        obj_func,
        distribution_sample,
        sampler=None,  # assuming it takes in a trained base sampler
        num_steps=10,
        starting_percentile=0.5,
        trials_per_percentile=100,
        total_trials=None):
    """
    assuming either `base_sampler` is already trained or `distribution_sample`
    is given
    """
    if total_trials is not None:
        trials_per_percentile = int(total_trials / num_steps)

    if sampler is None or sampler == "gmm":
        sampler = GMM()
    elif sampler == "dependencytree":
        sampler = MIDependencyTree(mixture.GMM())

    iteration = distribution_sample
    for percentile in np.linspace(starting_percentile, 0, num_steps):
        # fit previous iteration
        sampler.fit(iteration)
        # generate `sample_size` more
        iteration = sampler.sample(trials_per_percentile)
        # compute obj value
        iteration_values = np.array([obj_func(trial) for trial in iteration])
        # select `percentile` bottom (since we are minimizing)
        cutoff = np.percentile(iteration_values, percentile * 100)
        idx = iteration_values <= cutoff
        # repeat
        iteration = iteration[idx]
    return iteration[0]
