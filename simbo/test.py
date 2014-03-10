from time import time
import numpy as np
import pandas as pd
from sklearn.mixture import GMM
from sklearn.neighbors import KernelDensity

from demo_functions import *
from optimize import minimize
from generative_models import CountGenerator, MIDependencyTree, BucketConditionalGenerator

gmm = GMM()
kde = KernelDensity()
count = CountGenerator()
mi_tree_gmm = MIDependencyTree(GMM())
count_tree = MIDependencyTree(
    root_generator=CountGenerator(),
    cond_generator=BucketConditionalGenerator(CountGenerator())
)

# tuples of (name, method, options)
REAL_SOLVERS = [
    ("None", None, {}),
    ('Powell', "Powell", {}),
    ('Anneal', "Anneal", {}),
    ("rhc sa", "rhc", dict(method="Anneal")),
    ("rhc powell", "rhc", dict(method="Powell")),
    ("genetic", "genetic", dict(domain="gaussian")),
    ("twiddle", "twiddle", {}),
]

BINARY_SOLVERS = [
    ("MIMIC gmm", "MIMIC", dict(sampler=gmm, domain="binary")),
    ("MIMIC kde", "MIMIC", dict(sampler=kde, domain="binary")),
    # ("MIMIC MI tree gmm", "MIMIC", dict(sampler=mi_tree_gmm, domain="binary")),
    ("MIMIC count", "MIMIC", dict(sampler=count, domain="binary")),
    ("MIMIC count tree", "MIMIC", dict(sampler=count_tree, domain="binary")),
    ("genetic binary", "genetic", dict(domain="binary")),
    ("A/B test", "ab_test", {}),
]

def solve(fun, num_features, true_fun=None, domain="binary", maxiter=1000):
    solvers = (REAL_SOLVERS + BINARY_SOLVERS
               if domain == "binary" else REAL_SOLVERS)

    x0 = np.zeros(num_features)

    names = []
    columns = ["time", "score"]
    times = []
    scores = []
    for name, method, options in solvers:
        names.append(name)
        options["maxiter"] = maxiter
        start_time = time()
        result = minimize(fun, x0, method=method, options=options)
        total_time = time() - start_time
        times.append(total_time)
        if true_fun is None:
            scores.append(result.fun)
        else:
            scores.append(true_fun(result.x))
    return zip(names, times, scores)

# TODO show graph of expected value vs num trials


def binary_logistic_fun(num_features=100, noise_std=1):
    # convex objective function
    weights = normal_weights(num_features)
    init_func = linear_model(weights, 0)
    true_fun = apply_result(init_func, sigmoid)
    fun = apply_result(init_func,
                            gaussian_noise(noise_std),
                            sigmoid,
                            binary_with_prob,
                            # to_binary,
    )
    # converting input to binary
    fun = apply_input(fun, to_binary)
    return fun, true_fun


if __name__ == "__main__":
    num_features = 10
    fun, true_fun = binary_logistic_fun(num_features, 1)
    res = solve(fun, num_features, true_fun, "binary", 1000)
    for line in res:
        print line
