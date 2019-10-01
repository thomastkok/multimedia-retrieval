from .helpers import (
    translate_to_origin, scale_to_unit, align_to_eigenvectors
)


def normalization(meshes):
    for mesh in meshes:
        translate_to_origin(mesh)
        align_to_eigenvectors(mesh)
        scale_to_unit(mesh)
