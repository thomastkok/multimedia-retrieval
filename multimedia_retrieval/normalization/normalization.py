import pandas as pd

from .feat_norm import (
    normalize_histogram, normalize_histograms, standardize, standardize_to)
from .mesh_norm import (align_to_eigenvectors, flip_mesh, scale_to_unit,
                        translate_to_origin)


def mesh_norm(mesh):
    """Normalizes a single mesh."""
    new_mesh = translate_to_origin(mesh)
    new_mesh = align_to_eigenvectors(new_mesh)
    new_mesh = flip_mesh(new_mesh)
    new_mesh = scale_to_unit(mesh)
    return new_mesh


def mesh_normalization(meshes):
    """Normalizes all given meshes."""
    if not hasattr(meshes, '__iter__'):
        meshes = [meshes]
    meshes[:] = [mesh_norm(mesh) for mesh in meshes]


def feature_normalization(feature):
    """Normalizes the given feature."""
    if isinstance(feature[0], tuple):
        feature = normalize_histograms(feature)
    else:
        feature = standardize(feature)
    return feature


def features_normalization(features):
    """Normalizes all given features."""
    for feature in features:
        feature = feature_normalization(feature)
    return features


def normalize_to(values, norm_info):
    """Normalizes a set of feature values to correspond to the dataset."""
    new_values = {}
    for name, value in values.items():
        if isinstance(value, tuple):
            new_values[name] = normalize_histogram(value)
        else:
            new_values[name] = standardize_to(value,
                                              norm_info[name]['mean'],
                                              norm_info[name]['sd'])
    return pd.Series(new_values)
