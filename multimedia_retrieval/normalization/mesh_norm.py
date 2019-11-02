import open3d
import trimesh
import numpy as np

from math import pi

from multimedia_retrieval.mesh_conversion.helpers import mesh_to_trimesh


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


def compute_angle(v1, v2):
    """
    Computes the angle between two vectors in radians.
    """
    cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    angle = np.arccos(cos_angle)

    return angle


def align_eigen_to_axis(mesh, axs, ev):
    """
    Aligns one eigen vector to a predefined axis.
    It uses a rotation of the axis-angle representation.
    In order to obtain the axis of rotation we compute the cross product
    Then, we normalize it so we get a unit vector
    Then, the product of the angle and this normalized unit vector
    equals the rotation vector that we can use to align the
    eigenvalues with the axes.
    """
    rot_axis = np.cross(ev, axs)
    unit_rot_axis = rot_axis / np.linalg.norm(rot_axis)
    angle = compute_angle(ev, axs)
    axis_angle = angle * unit_rot_axis
    mesh.rotate(axis_angle, type=open3d.geometry.RotationType.AxisAngle)


def align_to_eigenvectors(mesh):
    """
    Aligns the mesh,
    such that its eigenvectors are the same direction as the axes.
    """
    x = np.asarray([1, 0, 0])
    y = np.asarray([0, 1, 0])

    vertices = np.asarray(mesh.vertices)
    eigenvectors = np.linalg.eigh(np.cov(vertices, rowvar=False))[1]

    align_eigen_to_axis(mesh, x, eigenvectors[:, 2])

    vertices = np.asarray(mesh.vertices)
    eigenvectors = np.linalg.eigh(np.cov(vertices, rowvar=False))[1]

    align_eigen_to_axis(mesh, y, eigenvectors[:, 1])


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
    flip = np.asarray(
        [[1.0, 0.0, 0.0, 0.0],
         [0.0, 1.0, 0.0, 0.0],
         [0.0, 0.0, 1.0, 0.0],
         [0.0, 0.0, 0.0, 1.0]]
    )
    for i, c in enumerate(mass):
        if c > 0:
            flip[i, i] = -1
    mesh.transform(flip)
