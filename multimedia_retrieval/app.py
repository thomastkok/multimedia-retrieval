import open3d

from .datasets.datasets import read_dataset
from .filter.filter import filter_meshes
from .interface.interface import create_interface
from .normalization.normalization import (feature_normalization,
                                          mesh_normalization)
from .visualization.visualization import draw_mesh, draw_meshes


def run():
    create_interface()
    # dataset = input('Please specify the dataset (princeton/labeled): ')
    # if not dataset:
    #     dataset = 'labeled'
    # meshes = read_dataset(dataset=dataset, n_meshes=10)
    # mesh_normalization(meshes.values())
    # for mesh in meshes.values():
    #     draw_mesh(mesh, draw_unit_cube=True)
    # draw_meshes(list(meshes.values()), draw_unit_cube=True)
