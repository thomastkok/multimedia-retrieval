import open3d

from .filter.filter import filter_meshes, refine_outlier
from .normalization.normalization import normalization
from .visualization.visualization import draw_mesh, draw_meshes
from .datasets.datasets import read_dataset, read_mesh
from .descriptors.descriptors import (compute_global_descriptors, 
                                      compute_diameter, 
                                      compute_eccentricity,
                                    compute_local_descriptors)

def run():
    dataset = input('Please specify the dataset (princeton/labeled): ')
    # filter_meshes(dataset, n_meshes=10000, output_file='test.csv')
    meshes = read_dataset(dataset=dataset, n_meshes=10)

    for mesh in meshes.values():
        compute_local_descriptors(mesh)

    # view_mesh = read_mesh('/home/ruben/Desktop/LabeledDB_new/Bust/306.off')
    # refined_mesh = refine_outlier(view_mesh, 20444, 20444*1.3, 20444/1.3, False)
    # draw_mesh(refined_mesh)

    # normalization(meshes.values())
    # draw_meshes(list(meshes.values()), draw_unit_cube=True)
