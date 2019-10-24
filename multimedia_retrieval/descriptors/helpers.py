import random
from math import pi, sqrt

import numpy as np
import open3d
import trimesh
import sys


def get_hist_ranges():
    return {
        'A3': (0, 180),
        'D1': (0, sqrt(3)),
        'D2': (0, sqrt(3)),
        'D3': (0, sqrt(3) / 2),
        'D4': (0, 1)
    }


def sample_points(mesh, sample_size, num_indices, func, **kwargs):
    """
    Samples n times random vertex points.
    It then applies a local descriptor function to these points.
    Returns the result of the applied function (of a local/global descriptor).
    """

    res = []
    verts_len = len(mesh.vertices)

    for i in range(sample_size):
        pts = random.sample(range(0, verts_len), num_indices)
        res.append(func(mesh, pts, **kwargs))
    return res


def get_eigen(mesh):
    """
    Get the eigenvalue and eigenvectors of the covariance matrix of a mesh.
    """

    vertices = mesh.vertices
    return np.linalg.eigh(np.cov(vertices, rowvar=False))


def compute_tetrahedron_volumes(mesh, sample_size):
    """
    Computes the cube root volume of a tetrahedron of four random points.
    """

    return sample_points(mesh, sample_size, 4, compute_tetrahedron_volume)


def compute_tetrahedron_volume(mesh, pts, **kwargs):
    """
    Computes the cube root of the volume of a tetrahedron.
    """

    verts = mesh.vertices

    v1 = verts[pts[0]]
    v2 = verts[pts[1]]
    v3 = verts[pts[2]]
    v4 = verts[pts[3]]

    v1v4 = v1 - v4
    v2v4 = v2 - v4
    v3v4 = v3 - v4

    volume = np.cbrt(np.abs(np.dot(v1v4, (np.cross(v2v4, v3v4)))) / 6)
    return volume


def compute_triangle_areas(tri_mesh, sample_size):
    """
    Computes the surface area of a random face given by three random points.
    """
    return sample_points(tri_mesh, sample_size, 3, compute_triangle_area)


def compute_triangle_area(tri_mesh, pts, **kwargs):
    """
    Computes the surface area of a random face given by three random points.
    """

    verts = tri_mesh.vertices

    v1 = verts[pts[0]]
    v2 = verts[pts[1]]
    v3 = verts[pts[2]]

    arr = [np.asarray((v1, v2, v3))]

    return np.sqrt(np.asscalar(trimesh.triangles.area(arr)))


def compute_dist(mesh, pts, **kwargs):
    """
    Computes the norm of the difference between two vectors.
    This result is the equal to the distance between two vectors.
    """

    verts = mesh.vertices

    v1 = verts[pts[0]]
    v2 = []
    if kwargs:
        v2 = kwargs['centroid']
    else:
        v2 = verts[pts[1]]

    return np.linalg.norm(np.asarray(v1) - np.asarray(v2))


def compute_dists(mesh, sample_size, is_d1=True):
    """
    Compute the distances between two random sampled vertex coordinates.
    A variant on this is the distance between the centroid and a random point.
    """

    if is_d1:
        centroid = mesh.get_center()
        return sample_points(mesh, sample_size, 1, compute_dist,
                             centroid=centroid)
    else:
        return sample_points(mesh, sample_size, 2, compute_dist)


def compute_angles(mesh, sample_size):
    """
    Computes the angles between two vectors.
    """
    return sample_points(mesh, sample_size, 3, compute_angle)


def compute_angle(mesh, pts, **kwargs):
    """
    Computes the angle between two vectors.
    It is given by the following function:
    cos alpha = a * b / ||a||*||b||
    """

    verts = mesh.vertices

    v1 = verts[pts[0]]
    v2 = verts[pts[1]]
    v3 = verts[pts[2]]

    # Obtain the vector between v1 and v2 and v2 and v3.
    e = v1 - v2
    f = v2 - v3

    cos_angle = np.dot(e, f) / (np.linalg.norm(e) * np.linalg.norm(f))
    angle = np.arccos(cos_angle)

    # Convert radian to angles
    return np.degrees(angle)


def compute_compactness(tri_mesh):
    """
    Computes the compactness of a shape.
    The compactness is computed as the sphericity.
    The sphericity equals one if the shape is perfect sphere.
    """

    # Mesh should be watertight (and thus have a volume)
    if tri_mesh.is_volume:
        area = tri_mesh.area
        volume = tri_mesh.volume
        compactness = ((pi ** (1/3)) * (6 * volume)**(2/3)) / area

        return compactness

    else:
        raise ValueError("Cannot compute compactness. Mesh is not watertight.")


def compute_eccentricity(mesh):
    """
    Computes the eccentricity of a mesh.
    It is the ratio between the largest eigenvalue and the smallest eigenvalue.
    The eigenvalues are obtained from the covariance matrix of the shape.
    """

    val, vec = get_eigen(mesh)
    min_ev = val[0]
    max_ev = val[2]

    if min_ev == 0:
        min_ev += sys.float_info.min

    return max_ev / min_ev


def compute_diameter(mesh):
    """
    Approximates the diameter of a mesh.
    It computes minimum of the difference between the max and min coordinates.
    """
    return min(mesh.get_max_bound() - mesh.get_min_bound())
