from multimedia_retrieval.datasets.datasets import read_dataset, read_mesh
from multimedia_retrieval.normalization.normalization import (
    feature_normalization, mesh_normalization)

from .distances import euclidean


def query_shape(mesh_path, dataset_name):
    mesh = read_mesh(mesh_path)
    dataset = read_dataset(dataset_name.lower(), n_meshes=10)
    mesh_normalization([mesh])
    mesh_normalization(dataset.values())

    # TODO: Replace fake feature values with real feature values
    mesh_feat = [1]
    ds_feat = {}
    for data_point in dataset.keys():
        ds_feat[data_point] = [int(data_point) / 12]

    shapes = match_shapes(mesh, dataset, mesh_feat, ds_feat, k=3)
    return [dataset[key] for key in shapes]


def match_shapes(mesh, dataset, mesh_feat, ds_feat, k=None):
    # Get features for mesh
    # Get features for all meshes in dataset (pre-calculated)
    # For now, both are parameters
    # Compute distance between query mesh and all meshes in dataset
    results = {}
    for data_point in ds_feat:
        dist = euclidean(mesh_feat, ds_feat[data_point])
        results[data_point] = dist
    # Sort distances from low to high
    # Return the k best matching shapes
    if not k:
        return sorted(results, key=results.get)
    else:
        return sorted(results, key=results.get)[:k]
