import open3d

from multimedia_retrieval.datasets.datasets import read_dataset
from multimedia_retrieval.processing.processing import normalization_tool
from multimedia_retrieval.processing.helpers import unit_cube


def run():
    meshes = read_dataset(dataset='princeton', n_meshes=10)
    normalization_tool(meshes)
    open3d.visualization.draw_geometries(
        list(meshes.values()) +
        [unit_cube]
    )
