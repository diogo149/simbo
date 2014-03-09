import numpy as np
from demo_functions import *
from ab_test import binary_AB_test_optimizer
from mimic import mimic_optimizer
from scipy.optimize import minimize
from generate import CountGenerator, MIDependencyTree, BucketConditionalGenerator
from sklearn.mixture import GMM
from sklearn.neighbors import KernelDensity


SOLVERS = [
    'Nelder-Mead',
    'Powell',
    # 'CG',  # works poorly without derivative
    # 'BFGS',  # works poorly without derivative
    # 'Newton-CG',  # Jacobian required
    'Anneal',
    # 'L-BFGS-B',  # works poorly without derivative
    # 'TNC',  # works poorly
    # 'COBYLA',  # breaks down for higher dimensions
    # 'SLSQP',  # works poorly
    # 'dogleg',  # 'Newton-CG',  # Jacobian required
    # 'trust-ncg',  # 'Newton-CG',  # Jacobian required
]


def binary_results(true_func, best_ans, ans):
    ans = to_binary(ans)
    expected_value = true_func(ans)
    best_value = true_func(best_ans)
    feature_accuracy = (best_ans == ans).mean()
    print "Feature Accuracy: %s" % feature_accuracy
    print "Best Value:       %s" % best_value
    print "Solution Value:   %s" % expected_value
    return feature_accuracy, best_value, expected_value


def demo1(num_features=10, noise_std=1, total_trials=1000):
    # convex objective function
    weights = normal_weights(num_features)
    best_ans = (weights < 0) + 0
    print_results = lambda x: binary_results(true_func, best_ans, x)
    init_func = linear_model(weights, 0)
    true_func = apply_result(init_func, sigmoid)
    obj_func = apply_result(init_func,
                            gaussian_noise(noise_std),
                            sigmoid,
                            binary_with_prob,
                            # to_binary,
    )
    # converting input to binary
    obj_func = apply_input(obj_func, to_binary)

    print "Zeros"
    print_results(np.zeros(num_features))

    for solver in SOLVERS:
        print solver
        res = minimize(obj_func,
                       np.zeros(num_features),
                       method=solver,
                       tol=1e-15,
                       options=dict(maxiter=total_trials))
        print_results(res.x)

    print "A/B testing"
    ans = binary_AB_test_optimizer(num_features,
                                   obj_func,
                                   total_trials=total_trials)
    print_results(ans)

    print "MIMIC gmm"
    ans = mimic_optimizer(obj_func,
                          np.random.randn(100, num_features),
                          sampler=GMM(),
                          total_trials=total_trials)
    print_results(ans)

    print "MIMIC kde"
    ans = mimic_optimizer(obj_func,
                          np.random.randn(100, num_features),
                          sampler=KernelDensity(),
                          total_trials=total_trials)
    print_results(ans)

    print "MIMIC count"
    ans = mimic_optimizer(obj_func,
                          np.random.randn(100, num_features),
                          sampler=MIDependencyTree(CountGenerator()),
                          total_trials=total_trials)
    print_results(ans)

    print "MIMIC count + cond count"
    ans = mimic_optimizer(obj_func,
                          np.random.randn(100, num_features),
                          sampler=MIDependencyTree(root_generator=CountGenerator(),
                                                   cond_generator=BucketConditionalGenerator(CountGenerator())),
                          total_trials=total_trials)
    print_results(ans)

# TODO show graph of expected value vs num trials
