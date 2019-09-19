import open3d

import multimedia_retrieval.datasets.datasets as datasets
from multimedia_retrieval.processing.processing import filter_meshes


def run():
    dataset = input('Please specify the dataset (princeton/labeled): ')
    filter_meshes(dataset, n_meshes=10, output_file='test.csv')
