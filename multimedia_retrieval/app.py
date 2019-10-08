import open3d

from .filter.filter import filter_meshes, refine_outlier
from .normalization.normalization import (mesh_normalization, 
                                         feature_normalization)
from .visualization.visualization import draw_mesh, draw_meshes
from .datasets.datasets import read_dataset, read_mesh
from .descriptors.descriptors import (compute_global_descriptors, 
                                      compute_diameter, 
                                      compute_eccentricity,
                                    compute_local_descriptors)


def run():
    dataset = input('Please specify the dataset (princeton/labeled): ')
    if not dataset:
        dataset = 'labeled'
    meshes = read_dataset(dataset=dataset, n_meshes=10)
    mesh_normalization(meshes.values())
    for mesh in meshes.values():
        draw_mesh(mesh, draw_unit_cube=True)
    draw_meshes(list(meshes.values()), draw_unit_cube=True)
