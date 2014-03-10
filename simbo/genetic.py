from functools import partial
import numpy as np

from optimize_utils import *


def initial_population(domain, size):
    if domain == "binary":
        return np.random.randint(2, size=size)
    elif domain == "gaussian":
        return np.random.randn(*size)
    else:
        raise ValueError("Unknown domain: %s" % domain)

def child_generation(p1, p2):
    selection_matrix = np.random.randint(2, size=p1.shape)
    return p1 * selection_matrix + p2 * (1 - selection_matrix)


def binary_mutation(population, mutation_rate):
    mutation_matrix = np.random.uniform(size=population.shape)
    mutation_matrix = (mutation_matrix < mutation_rate).astype(np.int)
    population ^= mutation_matrix
    return population


def gaussian_mutation(population, mutation_rate):
    return population + mutation_rate * np.random.randn(*population.shape)


MUTATIONS = dict(binary=binary_mutation,
                 gaussian=gaussian_mutation)


def mutation_function(domain, mutation_rate):
    return partial(MUTATIONS[domain], mutation_rate=mutation_rate)


def _minimize_genetic(fun,
                      x0,  # only used to get number of features
                      args=(),
                      callback=None,
                      cutoff_percentile=0.2,
                      decrease_percentile=True,
                      n_iter=100,
                      domain="binary",
                      mutation_rate=0.05,
                      batch_size=100,
                      maxiter=None,
                      keep_best=True):
    """
    genetic algorithm

    TODO
    - have convergence criteria
    """
    if maxiter is not None:
        n_iter = int(maxiter / batch_size)

    best = None
    best_score = float("inf")
    population = None
    mutate = mutation_function(domain, mutation_rate)
    for percentile in np.linspace(cutoff_percentile, 0, n_iter):
        if population is None:
            population = initial_population(domain, (batch_size, len(x0)))
        else:
            # create child generation
            p1 = parents[np.random.choice(len(parents), batch_size, True)]
            p2 = parents[np.random.choice(len(parents), batch_size, True)]
            population = child_generation(p1, p2)
            # perform mutation
            population = mutate(population)
        # score population
        scores = score_multi(fun, population, args, callback)
        if not decrease_percentile:
            percentile = cutoff_percentile
        # find parent generation
        cutoff = np.percentile(scores, percentile * 100)
        idx = scores <= cutoff
        parents = population[idx]

        # store best
        if keep_best:
            for trial, score in zip(population, scores):
                if score <= best_score:
                    best_score = score
                    best = trial

    if keep_best:
        x = best
        fval = best_score
    else:
        x = parents[0]
        fval = scores[idx[0]]
    nfev = n_iter * batch_size
    return to_result(x=x, fun=fval, niter=n_iter, nfev=nfev)
