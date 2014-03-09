import numpy as np
from abba.stats import Experiment as ABExperiment


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


def binary_AB_test_optimizer(num_features,
                             objective_function,
                             num_trials=None,
                             total_trials=None,
                             max_p_value=0.05):
    """
    sequential A/B testing simulation to minimize an objective function that
    returns 0/1

    assumptions:
    -the order of variables to be tested is left to right
    -the baseline solution is all zeros

    parameters:
    `num_features` : number of binary features the objective function takes
    `objective_function` : function whose value we want to minimize
    `confidence_level` : the desired p value
    `num_trials` : experiments to run for each of the baseline and variation
    `total_trials` : total number of trials (note: rounds down)
    """
    if total_trials is not None:
        num_trials = int(total_trials / num_features / 2)

    baseline = np.zeros(num_features)
    for i in range(num_features):
        baseline_success = 0
        variation_success = 0
        variation = baseline.copy()
        variation[i] = 1 - variation[i] # change 0 to 1 or 1 to 0
        for _ in range(num_trials):
            baseline_success += objective_function(baseline)
            variation_success += objective_function(variation)
        p_value, improvement = ab_test(baseline_success,
                                       num_trials,
                                       variation_success,
                                       num_trials)
        if p_value <= max_p_value and improvement < 0:
            baseline[i] = 1 - baseline[i]
    return baseline
