import open3d

from multimedia_retrieval.processing.processing import (normalization_tool,
                                                        filter_meshes)
from multimedia_retrieval.processing.helpers import unit_cube


def run():
    dataset = input('Please specify the dataset (princeton/labeled): ')
    filter_meshes(dataset, n_meshes=10, output_file='test.csv')
