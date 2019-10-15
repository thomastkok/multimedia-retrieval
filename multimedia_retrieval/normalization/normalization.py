from .mesh_norm import (
    translate_to_origin, scale_to_unit, align_to_eigenvectors, flip_mesh
)
from .feat_norm import rescale, standardize, normalize_histogram


def mesh_normalization(meshes):
    """Normalizes all given meshes."""
    if not hasattr(meshes, '__iter__'):
        meshes = [meshes]
    for mesh in meshes:
        translate_to_origin(mesh)
        align_to_eigenvectors(mesh)
        flip_mesh(mesh)
        scale_to_unit(mesh)


def feature_normalization(features):
    """Normalizes all given features."""
    if not isinstance(features, list):
        features = [features]
    for feature in features:
        if isinstance(feature, tuple):
            normalize_histogram(feature)
        else:
            standardize(feature)
    return features
