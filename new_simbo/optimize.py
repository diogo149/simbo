import numpy as np
from scipy.optimize import minimize as sp_minimize
from mimic import _minimize_mimic
from genetic import _minimize_genetic
from greedy import _minimize_rhc, _minimize_twiddle
from ab_test import _minimize_ab_test
from optimize_utils import to_result


SCIPY_METHODS = [
    'Nelder-Mead',
    'Powell',
    'CG',
    'BFGS',
    'Newton-CG',
    'Anneal',
    'L-BFGS-B',
    'TNC',
    'COBYLA',
    'SLSQP',
    'dogleg',
    'trust-ncg',
]

### minimize wrapper

def minimize(fun, x0, args=(), method='BFGS', jac=None, hess=None,
             hessp=None, bounds=None, constraints=(), tol=None,
             callback=None, options=None):
    """
    wrapper around scipy.optimize.minimize with extra functions
    """
    if method in SCIPY_METHODS:
        return sp_minimize(fun, x0, args, method, jac, hess, hessp, bounds,
                           constraints, tol, callback, options)
    if options is None:
        options = {}

    if method is None:
        res = to_result(x=x0, fun=fun(x0, *args), niter=1, nfev=1)
        if callback is not None:
            callback(x0)
        return res
    if method == "MIMIC":
        return _minimize_mimic(fun, x0, args, callback=callback, **options)
    elif method == "genetic":
        return _minimize_genetic(fun, x0, args, callback=callback, **options)
    elif method == "rhc":
        return _minimize_rhc(fun, x0, args, callback=callback, options=options)
    elif method == "ab_test":
        return _minimize_ab_test(fun, x0, args, callback=callback, **options)
    elif method == "twiddle":
        return _minimize_twiddle(fun, x0, args, callback=callback, **options)
    else:
        raise ValueError("Unknown solver: %s" % method)
