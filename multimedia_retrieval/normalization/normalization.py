from .mesh_norm import (
    translate_to_origin, scale_to_unit, align_to_eigenvectors, flip_mesh
)
from .feat_norm import rescale


def mesh_normalization(meshes):
    for mesh in meshes:
        translate_to_origin(mesh)
        align_to_eigenvectors(mesh)
        flip_mesh(mesh)
        scale_to_unit(mesh)


def feature_normalization(features):
    for feature in features:
        rescale(feature)
