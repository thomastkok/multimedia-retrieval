import open3d
import pandas as pd
import numpy as np

from .datasets.datasets import (read_dataset, read_mesh,
                                read_cache, write_cache)
from .descriptors.descriptors import (compute_global_descriptors,
                                      compute_local_descriptors)

from .filter.filter import filter_meshes, refine_outlier
from .interface.interface import create_interface
from .normalization.normalization import (feature_normalization,
                                          mesh_normalization)
from .visualization.visualization import draw_mesh, draw_meshes

from .histograms.histograms import plot_histogram


def run():
    cache = input('Read from cache (yes/no)?\n')
    if cache.lower().startswith('yes'):
        features, paths, norm_info = read_cache()
        print('Read from cache.')
    else:
        features, paths, norm_info = initialize()
        cache = input('Write to cache (yes/no)?\n')
        if cache.lower().startswith('y'):
            write_cache(features, paths, norm_info)
            print('Wrote to cache.')

    create_interface(features, paths, norm_info)


def initialize():
    """
    Reads the shapes, creates a feature dataset,
    and returns the feature datasets, paths for all shapes,
    and necessary information to normalize features of other shapes.
    """
    f = {}
    p = {}
    n = {}
    for dataset in ('princeton', 'labeled'):
        features, paths = read_dataset(dataset=dataset,
                                       n_meshes=10, features=True)
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
