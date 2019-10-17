import pandas as pd

from multimedia_retrieval.datasets.datasets import read_dataset, read_mesh
from multimedia_retrieval.descriptors.descriptors import \
    compute_global_descriptors
from multimedia_retrieval.normalization.normalization import (
    feature_normalization, mesh_normalization, normalize_to)

from .distances import euclidean


def query_shape(mesh_path, dataset_features, norm_info):
    """
    Given the file path to a local mesh, the features of the dataset,
    and the necessary information needed to normalize the query mesh,
    returns the closes matching shapes from the dataset.
    """
    mesh = read_mesh(mesh_path)
    mesh_normalization(mesh)
    mesh_features = compute_global_descriptors(mesh)
    mesh_features = normalize_to(mesh_features, norm_info)

    shapes = match_shapes(mesh_features, dataset_features, k=3)
    return shapes


def match_shapes(mesh_features, dataset_features, k=None):
    """
    Given the features for a mesh, a dataset of features, and k,
    returns the k closest feature sets in the dataset to
    the original mesh feature set.
    """
    results = {}
    for data_point in dataset_features:
        dist = euclidean(mesh_features, dataset_features[data_point])
        results[data_point] = dist

    shapes = pd.Series(results).sort_values()
    if not k:
        return shapes
    else:
        return shapes[:k]
