import pandas as pd

from multimedia_retrieval.datasets.datasets import read_dataset, read_mesh
from multimedia_retrieval.descriptors.descriptors import \
    compute_global_descriptors
from multimedia_retrieval.normalization.normalization import (
    feature_normalization, mesh_normalization, normalize_to)

from .distances import euclidean


def query_shape(mesh_path, dataset_features, norm_info):
    mesh = read_mesh(mesh_path)
    mesh_normalization(mesh)
    mesh_features = compute_global_descriptors(mesh)
    print(mesh_features)
    mesh_features = normalize_to(mesh_features, norm_info)
    print(mesh_features)

    shapes = match_shapes(mesh_features, dataset_features, k=3)
    return shapes


def match_shapes(mesh_features, dataset_features, k=None):
    # Get features for mesh
    # Get features for all meshes in dataset (pre-calculated)
    # For now, both are parameters
    # Compute distance between query mesh and all meshes in dataset
    results = {}
    for data_point in dataset_features:
        dist = euclidean(mesh_features, dataset_features[data_point])
        results[data_point] = dist
    # Sort distances from low to high
    # Return the k best matching shapes
    shapes = pd.Series(results).sort_values()
    if not k:
        return shapes
    else:
        return shapes[:k]
