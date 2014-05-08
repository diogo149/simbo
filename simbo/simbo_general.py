import heapq
from sklearn.dummy import DummyRegressor

import optimize_utils
import generative_models


def percentile_selector(percentile=0.5):
    def selector(results, batch):
        num = int(len(results) * percentile)
        selected_w_score = heapq.nsmallest(num, zip(results, batch),
                                           key=lambda x: x[0])
        return [v for score, v in selected_w_score]


def _minimize_simbo_general(fun,
                            x0,  # only used to get number of features
                            args=(),
                            callback=None,
                            batch_size=100,
                            population_size=10000,
                            maxiter=10000,
                            scorer=None, # if no scorer given, scores are constant
                            selector=None, # only relevant is sampler is given
                            sampler=None):
    n_iter = int(maxiter / batch_size)
    assert n_iter > 0

    dummy_generator = generative_models.DummyGenerator(len(x0))

    if scorer is None:
        scorer = DummyRegressor()
    if sampler is None:
        sampler = dummy_generator

    if isinstance(selector, float) and 0 < selector < 1:
        selector = percentile_selector(selector)

    for i in range(n_iter):
        if i == 0:
            batch = dummy_generator.sample(batch_size)
        else:
            population = sampler.sample(population_size)
            scores = scorer.predict(population)
            batch_w_score = heapq.nsmallest(batch_size, zip(scores, population),
                                            key=lambda x: x[0])
            batch = [v for score, v in batch_w_score]
        results = optimize_utils.score_multi(fun, batch, args, callback)
        selected = selector(results, batch) if selector is not None else batch
        scorer.fit(batch, results)
        sampler.fit(selected)

    best_fval, best_x = max(zip(results, batch), key=lambda x: x[0])
    nfev = batch_size * n_iter
    return optimize_utils.to_result(x=best_x, fun=best_fval,
                                    niter=n_iter, nfev=nfev)
