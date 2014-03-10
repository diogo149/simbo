import numpy as np
from functools import wraps


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def binary_with_prob(x):
    return 0 + (np.random.uniform(size=x.shape) <= x)


def to_binary(x, threshold=0):
    # not setting equal to so that to_binary of binary values doesn't change
    # the values
    return 0 + (x > threshold)


def apply_result(func, *to_apply):
    @wraps(func)
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        for f in to_apply:
            result = f(result)
        return result
    return inner


def apply_input(func, *to_apply):
    @wraps(func)
    def inner(x):
        for f in to_apply:
            x = f(x)
        return func(x)
    return inner


def gaussian_noise(std):
    def inner(x):
        return x + std * np.random.randn(*x.shape)
    return inner


def normal_weights(num_features,
                  mean=0,
                  std=1):
    # mean and std can be numpy arrays
    return mean + np.random.randn(num_features) * std


def linear_model(weights, constant):
    def inner(parameters):
        return weights.dot(parameters) + constant
    return inner
