# TODO rename Result to OptimizeResult when scipy is updated
import numpy as np
from scipy.optimize import Result as OptimizeResult


def to_result(x, fun, niter, nfev, status=0, success=True, message=""):
    return OptimizeResult(x=x, fun=fun, niter=niter, nfev=nfev,
                          status=status, success=success, message=message)

def score_multi(fun, xs, args=(), callback=None):
    scores = []
    for x in xs:
        scores.append(fun(x, *args))
        if callback is not None:
            callback(x)
    return scores
