import open3d

from .filter.filter import filter_meshes
from .normalization.normalization import normalization
from .visualization.visualization import draw_meshes, draw_mesh
from .datasets.datasets import read_dataset


def run():
    dataset = input('Please specify the dataset (princeton/labeled): ')
    if not dataset:
        dataset = 'labeled'
    meshes = read_dataset(dataset=dataset, n_meshes=10)
    normalization(meshes.values())
    for mesh in meshes.values():
        draw_mesh(mesh, draw_unit_cube=True)
    draw_meshes(list(meshes.values()), draw_unit_cube=True)
