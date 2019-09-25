import open3d

from multimedia_retrieval.processing.processing import filter_meshes
from multimedia_retrieval.processing.helpers import (
    unit_cube, normalization_tool)


def run():
    dataset = input('Please specify the dataset (princeton/labeled): ')
    filter_meshes(dataset, n_meshes=100, output_file='test.csv')
