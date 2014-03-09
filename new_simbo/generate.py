from copy import deepcopy
from collections import defaultdict
import numpy as np
import networkx as nx
from sklearn.base import BaseEstimator
from sklearn.metrics import mutual_info_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.mixture import GMM
from sklearn.neighbors import KernelDensity


class CountGenerator(BaseEstimator):
    """
    generates values by taking counts

    assumptions:
    - uniform prior
    """
    def __init__(self, prior=0):
        self.prior = prior

    def fit(self, X):
        values = defaultdict(lambda: 0)
        for obs in X:
            values[tuple(obs)] += 1
        choices = []
        probs = []
        for k, v in values.items():
            choices.append(k)
            probs.append(v)
        self.choices_ = np.array(choices)
        self.probs_ = np.array(probs, dtype=np.float)
        self.probs_ /= self.probs_.sum()
        return self

    def sample(self, n_samples=1, random_state=None):
        idxs = np.random.choice(np.arange(len(self.probs_)),
                                size=n_samples,
                                replace=True,
                                p=self.probs_)
        return self.choices_[idxs]


class BucketConditionalGenerator(BaseEstimator):
    """
    generates conditional values by creating a separate bucket for each unique
    sequence of values in the conditioning variables, and fits a generator on
    the contents of each bucket

    assumptions:
    - y (variable to be generated) is 1-d
    """
    def __init__(self, generator=None):
        if generator is None:
            generator = CountGenerator()
            # generator = GMM()
        self.generator = generator

    def new_generator(self, X):
        gen = deepcopy(self.generator)
        gen.fit(X)
        return gen

    def fit(self, X, y):
        y = y.reshape(-1, 1)  # this is the only part that requires 1-d y
        grouped = defaultdict(list)
        for obs, res in zip(X, y):
            grouped[tuple(obs)].append(res)
        self.generators_ = {}
        for key, values in grouped.items():
            self.generators_[key] = self.new_generator(values)
        self.backup_gen = self.new_generator(y)
        return self

    def sample(self, X, random_state=None):
        samples = [self.sample_one(obs, random_state) for obs in X]
        return np.array(samples)

    def sample_one(self, x, random_state=None):
        # not using random state
        key = tuple(x)
        if key in self.generators_:
            res = self.generators_[key].sample(1).flatten()
            return res
        else:
            return self.backup_gen.sample(1).flatten()


class ConditionalGenerator(BaseEstimator):
    """
    creates a conditional generator from a joint distribution generator

    in order to sample from the conditional distribution for x given y, we
    first generate samples for both variables, then selects

    `cond_samples` : samples to generate for conditional distribution estimation

    assumptions:
    - variable to be sampled is 1 dimensional

    TODO:
    - parameterize method of selecting which sample(s) are used to use
      supervised learning techniques (k-NN, etc.)
    - allow for higher dimensional sampled variables
    """
    def __init__(self,
                 generator=None,
                 cond_samples=100):
        if generator is None:
            generator = GMM()
        self.generator = generator
        self.cond_samples = cond_samples

    def fit(self, X, y):
        stacked = np.hstack((X, y.reshape(-1, 1)))
        self.generator.fit(stacked)
        return self

    def sample(self, X, random_state=None):
        joint = self.generator.sample(self.cond_samples, random_state)
        joint_X, joint_y = joint[:, :-1], joint[:, -1]
        knn = KNeighborsRegressor(1)
        knn.fit(joint_X, joint_y)
        return knn.predict(X)


class MIDependencyTree(BaseEstimator):
    """
    `root_generator` : generator for the root variable
    `cond_generator` : conditional generator (implementing `fit` and `sample`)
    `bins` : bins for mutual information calculation

    assumptions:
    - first feature is root of the tree

    TODO:
    - parameterize Mutual Information out
    - parameterize how to generate given the parent in the tree
    - intelligent procedure for picking the root of the tree

    MI Calculation from:
    http://stackoverflow.com/questions/20491028/optimal-way-for-calculating-columnwise-mutual-information-using-numpy
    """
    def __init__(self,
                 root_generator=None,
                 cond_generator=None,
                 bins=10):
        if root_generator is None:
            root_generator = GMM()
        if cond_generator is None:
            cond_generator = ConditionalGenerator(deepcopy(root_generator))
        self.root_generator = root_generator
        self.cond_generator = cond_generator
        self.bins = bins

    def new_generator(self, X, y):
        gen = deepcopy(self.cond_generator)
        gen.fit(X, y)
        return gen

    def fit(self, X, y=None):
        self.num_feat_ = X.shape[1]
        g = nx.Graph()
        g.add_nodes_from(range(self.num_feat_))
        for i in range(self.num_feat_):
            for j in range(i + 1, self.num_feat_):
                c_xy = np.histogram2d(X[:, i], X[:, j], self.bins)[0]
                mi = mutual_info_score(None, None, contingency=c_xy)
                g.add_edge(i, j, weight=mi)
        t = nx.minimum_spanning_tree(g)
        self.edges_ = t.edges() # list of (i,j) tuples
        self.root_generator.fit(X[:, [0]])
        self.generators_ = [self.new_generator(X[:, [i]], X[:, [j]])
                            for i, j in self.edges_]
        return self

    def sample(self, n_samples=1, random_state=None):
        X = np.zeros((n_samples, self.num_feat_))
        X[:, 0] = self.root_generator.sample(n_samples, random_state).flatten()
        for (parent, child), gen in zip(self.edges_, self.generators_):
            X[:, child] = gen.sample(X[:, [parent]], random_state).flatten()
        return X

if __name__ == "__main__":
    # just trying it out
    gen = MIDependencyTree()
    x = 3 + 4 * np.random.randn(1000, 10)
    gen.fit(x)
    x2 = gen.sample(1000)
    print x.mean(), x.std(), x.min(), x.max()
    print x2.mean(), x2.std(), x.min(), x.max()
