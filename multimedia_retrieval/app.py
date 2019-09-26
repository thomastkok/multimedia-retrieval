import open3d

from multimedia_retrieval.filter.filter import filter_meshes
from multimedia_retrieval.normalization.normalization import normalization
from multimedia_retrieval.visualization.visualization import draw_meshes
from multimedia_retrieval.datasets.datasets import read_dataset


def run():
    dataset = input('Please specify the dataset (princeton/labeled): ')
    filter_meshes(dataset, n_meshes=10, output_file='test.csv')

    meshes = read_dataset(dataset=dataset, n_meshes=10)
    normalization(meshes.values())
    draw_meshes(list(meshes.values()), draw_unit_cube=True)
