import open3d
import pandas as pd
from numpy import mean, std

from .datasets.datasets import read_dataset, read_mesh
from .descriptors.descriptors import (compute_global_descriptors,
                                      compute_local_descriptors)
from .filter.filter import filter_meshes, refine_outlier
from .interface.interface import create_interface
from .normalization.normalization import (feature_normalization,
                                          mesh_normalization)
from .visualization.visualization import draw_mesh, draw_meshes


def run():
    features, paths, norm_info = initialize()

    create_interface(features, paths, norm_info)


def initialize():
    f = {}
    p = {}
    n = {}
    for dataset in ('princeton', 'labeled'):
        features, paths = read_dataset(dataset=dataset,
                                       n_meshes=10, features=True)
        norm_infos = {}

        for name, series in features.iterrows():
            norm_infos[name] = {
                'mean': mean(series),
                'sd': std(series),
                'min': min(series),
                'max': max(series)
            }
            feature_normalization([series])

        f[dataset] = features
        p[dataset] = paths
        n[dataset] = pd.DataFrame(norm_infos)
    return pd.Series(f), pd.Series(p), pd.Series(n)
