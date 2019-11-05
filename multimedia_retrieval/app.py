import numpy as np
import pandas as pd

from .datasets.datasets import read_cache, read_dataset, write_cache
from .evaluation.evaluation import evaluate, get_dist_mat, plot_conf_matrix
from .interface.interface import create_interface
from .normalization.normalization import feature_normalization


def run():
    datasets = ['labeled']
    cache = input('Read from cache (yes/no)?\n')
    if cache.lower().startswith('y'):
        features, paths, norm_info = read_cache(datasets)
        print('Read from cache.')
    else:
        print('Calculating feature values.')
        features, paths, norm_info = initialize(datasets)
        cache = input('Write to cache (yes/no)?\n')
        if cache.lower().startswith('y'):
            write_cache(features, paths, norm_info, datasets)
            print('Wrote to cache.')

    eval = input('Do you want to evaluate the querying (yes/no)?\n')
    if eval.lower().startswith('y'):
        cache = input('Read distance matrix from cache (yes/no)?\n')
        c = cache.lower().startswith('yes')
        distance_matrix = get_dist_mat(features['labeled'], c)
        plot_conf_matrix(features, distance_matrix)
        evaluate(features, paths, norm_info, distance_matrix)
    create_interface(features, paths, norm_info)


def initialize(datasets=['princeton', 'labeled']):
    """
    Reads the shapes, creates a feature dataset,
    and returns the feature datasets, paths for all shapes,
    and necessary information to normalize features of other shapes.
    """
    f = {}
    p = {}
    n = {}
    for dataset in datasets:
        features, paths = read_dataset(dataset=dataset,
                                       n_meshes=None, features=True)
        norm_infos = {}

        for name, series in features.iteritems():
            if not isinstance(series[0], tuple):
                norm_infos[name] = {
                    'mean': np.mean(series),
                    'sd': np.std(series),
                    'min': min(series),
                    'max': max(series)
                }
                features[name] = list(feature_normalization(series))
            else:
                features[name] = list(feature_normalization(series))

        f[dataset] = features
        p[dataset] = paths
        n[dataset] = pd.DataFrame(norm_infos)
    return pd.Series(f), pd.Series(p), pd.Series(n)
