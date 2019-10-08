import numpy as np
from scipy.stats import wasserstein_distance


def euclidean(one, two):
    if len(one) != len(two):
        raise ValueError('Length of both features must be the same')
    return np.linalg.norm(np.asarray(one) - np.asarray(two))


def cosine(one, two):
    if len(one) != len(two):
        raise ValueError('Length of both features must be the same')
    if min(one) < 0 or min(two) < 0 or max(one) > 1 or max(two) > 1:
        raise ValueError('Feature values must be between 0 and 1')
    one_arr = np.asarray(one)
    two_arr = np.asarray(two)
    return 1 - ((one_arr @ two_arr) /
                (np.linalg.norm(one_arr) * np.linalg.norm(two_arr)))


def earth_movers(one, two):
    if len(one) != len(two):
        raise ValueError('Length of both features must be the same')
    return wasserstein_distance(one, two)
