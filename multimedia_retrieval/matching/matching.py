from multimedia_retrieval.datasets.datasets import read_dataset, read_mesh
from multimedia_retrieval.descriptors.descriptors import \
    compute_global_descriptors
from multimedia_retrieval.normalization.normalization import (
    feature_normalization, mesh_normalization)

from .distances import euclidean


def query_shape(mesh_path, dataset, ds_features):
    mesh = read_mesh(mesh_path)
    mesh_normalization([mesh])
    mesh_features = compute_global_descriptors(mesh)
    feature_normalization(mesh_features)

    shapes = match_shapes(mesh_features, ds_features, k=3)
    print(dataset)
    print([key for key in shapes])
    return [dataset[key] for key in shapes]


def match_shapes(mesh_features, ds_features, k=None):
    # Get features for mesh
    # Get features for all meshes in dataset (pre-calculated)
    # For now, both are parameters
    # Compute distance between query mesh and all meshes in dataset
    results = {}
    for data_point in ds_features:
        dist = euclidean(mesh_features, ds_features[data_point])
        results[data_point] = dist
    # Sort distances from low to high
    # Return the k best matching shapes
    if not k:
        return sorted(results, key=results.get)
    else:
        return sorted(results, key=results.get)[:k]
