import open3d
import numpy as np


def translate_to_origin(mesh):
    """
    Translates the mesh,
    such that its centroid coincides with the coordinate-frame origin.
    """
    mesh.translate(-mesh.get_center())


def scale_to_unit(mesh):
    """
    Scales the mesh,
    such that it fits tightly in a unit-sized cube.

    The mesh must be located at the origin.
    """
    center = mesh.get_center()
    if center[0] > 0.001 or center[1] > 0.001 or center[2] > 0.001:
        raise ValueError(
            f'Mesh must be centered around the origin, not {center}'
        )
    factor = 1 / max(mesh.get_max_bound() - mesh.get_min_bound())
    mesh.scale(factor, center=True)


def align_to_eigenvectors(mesh):
    """
    Aligns the mesh,
    such that its eigenvectors are the same direction as the axes.
    """
    vertices = np.asarray(mesh.vertices)
    eigenvectors = np.linalg.eigh(np.cov(vertices, rowvar=False))[1]
    mesh.vertices = open3d.utility.Vector3dVector(
                      np.stack([vertices @ eigenvectors[:, 0],
                                vertices @ eigenvectors[:, 1],
                                vertices @ eigenvectors[:, 2]], axis=1))


def flip_mesh(mesh):
    """
    Flips the mesh,
    such that the 'heaviest' side is always on the negative side of each axis.
    """
    mass = [0, 0, 0]
    for triangle in mesh.triangles:
        center = [0, 0, 0]
        for v in triangle:
            vertex = mesh.vertices[v]
            center += vertex
        center = center / 3
        for i, c in enumerate(center):
            mass[i] += np.sign(c) * (c * c)
    flip = [1, 1, 1]
    for i, c in enumerate(mass):
        if c > 0:
            flip[i] = -1
    for v in mesh.vertices:
        v = v * flip
