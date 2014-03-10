import numpy as np
from scipy.optimize import minimize

from optimize_utils import *


def _minimize_rhc(*args, **kwargs):
    # randomized hill-climbing
    options = kwargs["options"]
    method = options.pop("method")
    kwargs["method"] = method
    remaining = options["maxiter"]
    best_result = None
    while remaining > 0:
        options["maxiter"] = remaining
        result = minimize(*args, **kwargs)
        if best_result is None or best_result.fun > result.fun:
            best_result = result
        remaining -= result.nfev
    return best_result


def _minimize_twiddle(fun, x0, args=(), callback=None, tol=0.2, maxiter=1000):
    nfev = 0
    def score(x):
        # nfev += 1  # TODO uncomment when nonlocal keyword can be used
        res = fun(x, *args)
        if callback is not None:
            callback(x)
        return res

    p = x0.copy()
    num_params = len(p)
    dp = np.ones(num_params)
    best_err = score(p)
    nfev += 1
    stop = False
    n_iter = 0
    while dp.sum() > tol and not stop:
        n_iter += 1
        stop = True
        for i in range(num_params):
            p[i] += dp[i]
            err = score(p)
            nfev += 1
            if err < best_err:
                best_err = err
                dp[i] *= 1.1
            else:
                p[i] -= 2 * dp[i]
                err = score(p)
                nfev += 1
                if err < best_err:
                    best_err = err
                    dp[i] *= 1.1
                else:
                    p[i] += dp[i]
                    dp[i] *= 0.9
            # subtraction 1 since each loop is 2 iterations
            if nfev >= maxiter - 1:
                break
        else:
            stop = False
    return to_result(x=p, fun=best_err, niter=n_iter, nfev=nfev)
