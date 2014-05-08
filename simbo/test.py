from time import time
import numpy as np
from sklearn.mixture import GMM
from sklearn.neighbors import KernelDensity
from sklearn.linear_model import Ridge, SGDRegressor

from demo_functions import *
from optimize import minimize
from generative_models import CountGenerator, MIDependencyTree, BucketConditionalGenerator
from elm import ElmRegressor
import robot_simulation

gmm = GMM()
kde = KernelDensity()
count = CountGenerator()
mi_tree_gmm = MIDependencyTree(GMM())
count_tree = MIDependencyTree(
    root_generator=CountGenerator(),
    cond_generator=BucketConditionalGenerator(CountGenerator())
)
sgd = SGDRegressor()
elm = ElmRegressor(100)

# tuples of (name, method, options)
REAL_SOLVERS = [
    ("None", None, {}),
    ('Powell', "Powell", {}),
    ('Anneal', "Anneal", {}),
    ("rhc sa", "rhc", dict(method="Anneal")),
    ("rhc powell", "rhc", dict(method="Powell")),
    ("genetic", "genetic", dict(domain="gaussian")),
    ("twiddle", "twiddle", {}),
    ("simbo random", "simbo_general", {}),
    ("simbo gmm", "simbo_general", dict(sampler=gmm, selector=0.5)),
    ("simbo kde", "simbo_general", dict(sampler=kde, selector=0.5)),
    ("simbo sgd", "simbo_general", dict(scorer=sgd)),
    ("simbo elm", "simbo_general", dict(scorer=elm)),
    ("simbo gmm+sgd", "simbo_general", dict(sampler=gmm, selector=0.5, scorer=sgd)),
    ("simbo kde+sgd", "simbo_general", dict(sampler=kde, selector=0.5, scorer=sgd)),
    ("simbo gmm+elm", "simbo_general", dict(sampler=gmm, selector=0.5, scorer=elm)),
    ("simbo kde+elm", "simbo_general", dict(sampler=kde, selector=0.5, scorer=elm)),
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

def solve(fun, num_features, true_fun=None, domain="binary", maxiter=10000):
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


def robot_fun(noise=0.1):
    def f(params):
        return robot_simulation.run(params, noise)
    return f


def print_results(results):
    print("| Name | Time (s) | Score |")
    for name, time, score in results:
        print("| %s | %f | %s |" % (name, time, score))
    print("\n")


if __name__ == "__main__":
    if True:
        for num_features in [10, 100]:
            for noise in [1e-6, 1, 10]:
                print("Binary logisitc w/ {} features".format(num_features))
                fun, true_fun = binary_logistic_fun(num_features, noise)
                res = solve(fun, num_features, true_fun, "binary", 1000)
                print_results(res)

    if True:
        for noise in [0., 0.1, 10.0, 100.0]:
            print("Robot simulation w/ {} noise".format(noise))
            res = solve(robot_fun(noise), 3, None, "gaussian", 1000)
            print_results(res)
