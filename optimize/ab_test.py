import numpy as np
from abba.stats import Experiment as ABExperiment
from optimize_utils import *


def ab_test(baseline_num_successes,
            baseline_num_trials,
            num_successes,
            num_trials,
            num_variations=1,
            confidence_level=0.95):
    """
    num_variations: number of different variations of experiment
    """
    experiment = ABExperiment(num_variations,
                              baseline_num_successes,
                              baseline_num_trials,
                              confidence_level)
    results = experiment.get_results(num_successes, num_trials)
    rel_improvement = results.relative_improvement
    p_value = results.two_tailed_p_value
    return p_value, rel_improvement.value


def _minimize_ab_test(fun,
                      x0,
                      args=(),
                      callback=None,
                      num_trials=100,
                      maxiter=1000,
                      max_p_value=0.05):
    """
    sequential A/B testing simulation to minimize an objective function that
    returns 0/1

    assumptions:
    -the order of variables to be tested is left to right
    -the baseline solution is all zeros

    parameters:
    `confidence_level` : the desired p value
    `num_trials` : experiments to run for each of the baseline and variation
    `maxiter` : total number of trials (note: rounds down)
    """
    num_features = len(x0)
    if maxiter is not None:
        num_trials = int(maxiter / num_features / 2)

    baseline = x0.copy()
    if num_trials < 1:
        return baseline

    def score(x):
        res = fun(x, *args)
        if callback is not None:
            callback(x)
        return res

    for i in range(num_features):
        baseline_success = 0
        variation_success = 0
        variation = baseline.copy()
        variation[i] = 1 - variation[i] # change 0 to 1 or 1 to 0
        for _ in range(num_trials):
            baseline_success += score(baseline)
            variation_success += score(variation)
        p_value, improvement = ab_test(baseline_success,
                                       num_trials,
                                       variation_success,
                                       num_trials)
        if p_value <= max_p_value and improvement < 0:
            baseline[i] = 1 - baseline[i]
    error = float(baseline_success) / num_trials
    return to_result(x=baseline, fun=error, niter=num_trials,
                     nfev=num_trials * num_features)
