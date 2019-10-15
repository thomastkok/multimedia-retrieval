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
    dataset = 'labeled'
    meshes = read_dataset(dataset=dataset, n_meshes=10)
    mesh_normalization(meshes.values())

    ds_feat = {}
    for mesh in meshes.keys():
        ds_feat[mesh] = \
            compute_global_descriptors(meshes[mesh])
    features = pd.DataFrame(ds_feat)
    print(features)

    for name, series in features.iterrows():
        feature_normalization(series)
    print(features)
    create_interface(meshes, features)
