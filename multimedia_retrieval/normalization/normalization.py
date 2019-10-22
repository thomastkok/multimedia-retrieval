from .feat_norm import (normalize_histogram, normalize_histograms,
                        rescale, rescale_to, standardize,
                        standardize_to)
from .mesh_norm import (align_to_eigenvectors, flip_mesh, scale_to_unit,
                        translate_to_origin)
import pandas as pd


def mesh_normalization(meshes):
    """Normalizes all given meshes."""
    if not hasattr(meshes, '__iter__'):
        meshes = [meshes]
    for mesh in meshes:
        translate_to_origin(mesh)
        align_to_eigenvectors(mesh)
        flip_mesh(mesh)
        scale_to_unit(mesh)


def feature_normalization(feature):
    """Normalizes the given feature."""
    if isinstance(feature[0], tuple):
        feature = normalize_histograms(feature)
    else:
        standardize(feature)
    return feature


def features_normalization(features):
    for feature in features:
        feature_normalization(feature)
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
