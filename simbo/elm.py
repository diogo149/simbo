import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.pipeline import Pipeline


def relu(X):
    """Rectified Linear Unit"""
    return np.clip(X, 0, None)


def sigmoid(X):
    return 1 / (1 + np.exp(-X))


STR_TO_ACTIVATION = dict(
    relu=relu,
    sigmoid=sigmoid,
    tanh=np.tanh,
)


class ElmTransform(BaseEstimator, TransformerMixin):
    def __init__(self,
                 n_hidden,
                 activation_function="tanh",
                 std=1.0):
        self.n_hidden = n_hidden
        # assume it's a function if it is not in the dict
        self.activate_ = STR_TO_ACTIVATION.get(activation_function,
                                               activation_function)
        self.std = std

    def fit(self, X, y=None):
        X = np.array(X)
        self.weights_ = self.std * np.random.randn(X.shape[1], self.n_hidden)
        self.biases_ = self.std * np.random.randn(self.n_hidden)
        return self

    def transform(self, X, y=None):
        X = np.array(X)
        p = X.dot(self.weights_)
        return self.activate_(p + self.biases_)


def ElmRegressor(n_hidden, activation_function="tanh", std=1.0, **kwargs):
    return Pipeline([("elm", ElmTransform(n_hidden, activation_function, std)),
                     ("ridge", Ridge(**kwargs))])


def ElmClassifier(n_hidden, activation_function="tanh", std=1.0, **kwargs):
    return Pipeline([("elm", ElmTransform(n_hidden, activation_function, std)),
                     ("logreg", LogisticRegression(**kwargs))])
