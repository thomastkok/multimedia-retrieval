import sys
import numpy as np

from .helpers import (compute_angles, compute_compactness,
                      compute_diameter, compute_eccentricity,
                      compute_dists, get_eigen,
                      compute_triangle_areas,
                      compute_tetrahedron_volumes,
                      get_hist_ranges)

import numpy as np
import open3d
import pandas as pd
import trimesh

from multimedia_retrieval.histograms.histograms import plot_histogram
from multimedia_retrieval.mesh_conversion.helpers import (mesh_to_trimesh,
                                                          trimesh_to_mesh)

from .helpers import (compute_angles, compute_compactness, compute_diameter,
                      compute_dists, compute_eccentricity,
                      compute_tetrahedron_volumes, compute_triangle_areas,
                      get_eigen)


def compute_global_descriptors(mesh):
    """
    Computes the global descriptors as described by the assignment.
    Returns a dictionary containing the global descriptors.
    """
    tri_mesh = mesh_to_trimesh(mesh)

    global_features = {}
    global_features['surface_area'] = tri_mesh.area
    global_features['compactness'] = compute_compactness(tri_mesh)
    global_features['bb_volume'] = tri_mesh.bounding_box.volume
    global_features['diameter'] = compute_diameter(mesh)
    global_features['eccentricity'] = compute_eccentricity(mesh)

    return pd.Series(global_features)


def compute_local_descriptors(mesh, sample_size, nr_bins):
    """
    Computes the local descriptors as described by the assignment.
    Returns a dictionary containing the local descriptors.
    """

    hist_ranges = get_hist_ranges()

    a_3 = compute_angles(mesh, sample_size)
    d_1 = compute_dists(mesh, sample_size)
    d_2 = compute_dists(mesh, sample_size, False)
    d_3 = compute_triangle_areas(mesh, sample_size)
    d_4 = compute_tetrahedron_volumes(mesh, sample_size)

    local_features = {}
    local_features['A3'] = np.histogram(
        a_3, nr_bins, range=(hist_ranges['A3']))
    local_features['D1'] = np.histogram(
        d_1, nr_bins, range=(hist_ranges['D1']))
    local_features['D2'] = np.histogram(
        d_2, nr_bins, range=(hist_ranges['D2']))
    local_features['D3'] = np.histogram(
        d_3, nr_bins, range=(hist_ranges['D3']))
    local_features['D4'] = np.histogram(
        d_4, nr_bins, range=(hist_ranges['D4']))

    return pd.Series(local_features)
