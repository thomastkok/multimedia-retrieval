import open3d

from .datasets.datasets import read_dataset, read_mesh
from .descriptors.descriptors import (compute_global_descriptors,
                                      compute_local_descriptors)
from .filter.filter import filter_meshes, refine_outlier
from .normalization.normalization import (feature_normalization,
                                          mesh_normalization)
from .visualization.visualization import draw_mesh, draw_meshes


def run():
    dataset = input('Please specify the dataset (princeton/labeled): ')
    if not dataset:
        dataset = 'labeled'
    meshes = read_dataset(dataset=dataset, n_meshes=10)
    mesh_normalization(meshes.values())
    # filter_meshes(dataset)
    for mesh in meshes.values():
        compute_local_descriptors(mesh, len(mesh.vertices), 10)
        compute_global_descriptors(mesh)
    #     draw_mesh(mesh, draw_unit_cube=True)
    # draw_meshes(list(meshes.values()), draw_unit_cube=True)
