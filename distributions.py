import numpy as np


class ChoiceDistribution(object):
    def __init__(self, num_values):
        self.num_values = num_values

    def generate(self, points):
        return np.random.randint(0,
                                 self.num_values,
                                 points)


class BinaryDistribution(ChoiceDistribution):
    def __init__(self):
        super(BinaryDistribution, self).__init__(2)


DISTRIBUTIONS = dict(
    # choice=ChoiceDistribution,
    binary=BinaryDistribution,
)

DISTRIBUTIONS_SCHEMA = dict(
    # choice={"num_values": "int"},
    binary={},
)


def generate_random(distribution_type, params, points):
    distribution = DISTRIBUTIONS[distribution_type](**params)
    return distribution.generate(points)
