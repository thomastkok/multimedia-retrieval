import open3d

from multimedia_retrieval.processing.processing import (normalization,
                                                        filter_meshes)
from multimedia_retrieval.processing.helpers import (unit_cube,
                                                     align_to_eigenvectors)
from multimedia_retrieval.datasets.datasets import read_dataset


def run():
    dataset = input('Please specify the dataset (princeton/labeled): ')
    meshes = read_dataset(dataset=dataset, n_meshes=1)
    normalization(meshes.values())
    open3d.visualization.draw_geometries(
        list(meshes.values()) +
        [unit_cube()]
    )
