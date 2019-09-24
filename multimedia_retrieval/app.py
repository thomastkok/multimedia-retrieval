import open3d

from .filter.filter import filter_meshes
from .normalization.normalization import normalization
from .visualization.visualization import draw_meshes
from .datasets.datasets import read_dataset


def run():
    dataset = input('Please specify the dataset (princeton/labeled): ')
#    filter_meshes(dataset, n_meshes=10, output_file='test.csv')

    meshes = read_dataset(dataset=dataset, n_meshes=10)
    normalization(meshes.values())
    draw_meshes(list(meshes.values()), draw_unit_cube=True)
