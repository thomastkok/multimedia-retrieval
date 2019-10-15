import open3d
import pandas as pd

from .datasets.datasets import read_dataset, read_mesh
from .descriptors.descriptors import (compute_global_descriptors,
                                      compute_local_descriptors)
from .filter.filter import filter_meshes, refine_outlier
from .interface.interface import create_interface
from .normalization.normalization import (feature_normalization,
                                          mesh_normalization)
from .visualization.visualization import draw_mesh, draw_meshes


def run():
    features, paths = initialize()

    create_interface(features, paths)


def initialize():
    f = {}
    p = {}
    for dataset in ('princeton', 'labeled'):
        features, paths = read_dataset(dataset=dataset,
                                       n_meshes=10, features=True)

        for name, series in features.iterrows():
            feature_normalization(series)

        f[dataset] = features
        p[dataset] = paths
    return pd.Series(f), pd.Series(p)
