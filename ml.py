import numpy as np
from scipy.stats import norm
from sklearn.ensemble import RandomForestRegressor


def rf_factory():
    return RandomForestRegressor(
        # higher: more accuracy, less speed
        n_estimators=30,
        # higher: less stochastic, less speed, maybe less accuracy
        max_features='log2', # should use log2 or sqrt
        # higher: more accuracy, more overfitting, less speed, less stochastic
        max_depth=4,
        # higher: more speed, more stochastic, less accuracy, less overfitting
        # if too high, wouldn't be able to fit with less data
        min_samples_split=2,
        # higher: more speed, more stochastic, less accuracy, less overfitting
        # if too high, wouldn't be able to fit with less data
        min_samples_leaf=1,
        # True: more stochastic
        boostrap=True,
        # -1 or > 1: train in parallel
        n_jobs=1,
        # change to integer for reproducibility
        random_state=None,
    )


def expected_improvement(f_min, mu, sigma):
    """
    Takes in mu as an array of means and sigma as an
    array of standard deviations, and f_min the smallest value
    of the objective function so far (with parameter theta_incumbent).

    See http://www.cs.ubc.ca/~hutter/papers/11-LION5-SMAC.pdf
    """
    v = (np.log(f_min) - mu) / sigma
    return (f_min * norm.cdf(v)
            - (np.exp(0.5 * sigma ** 2 + mu)
               * norm.cdf(v - sigma)))


def random_forest_evaluate(rf, sample_points):
    """
    Return a vector of mean predictions for each of a set
    of input points, and a vector of the standard deviations
    for those predictions.
    """
    predictions = np.array(
        map(lambda x: x.predict(sample_points),
            rf.estimators_))
    mu = np.mean(preds, axis=0)
    sigma = np.std(preds, axis=0)
    return mu, sigma
