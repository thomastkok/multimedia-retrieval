import open3d

from .datasets.datasets import read_dataset, read_mesh
from .descriptors.descriptors import (compute_global_descriptors,
                                      compute_local_descriptors)

from .filter.filter import filter_meshes, refine_outlier
from .normalization.normalization import (feature_normalization,
                                          mesh_normalization)
from .visualization.visualization import draw_mesh, draw_meshes

from .histograms.histograms import plot_histogram


def run():
    dataset = input('Please specify the dataset (princeton/labeled): ')
    if not dataset:
        dataset = 'labeled'

    bust = read_mesh('/home/ruben/Desktop/LabeledDB_new/Bust/310.off')
    glasses = read_mesh('/home/ruben/Desktop/LabeledDB_new/Glasses/49.off')

    arm1 = read_mesh('/home/ruben/Desktop/LabeledDB_new/Armadillo/293.off')
    arm2 = read_mesh('/home/ruben/Desktop/LabeledDB_new/Armadillo/295.off')

    meshes = [arm1, arm2]
    mesh_normalization(meshes)

    # draw_mesh(arm1)
    # draw_mesh(arm2)

    # bust_global = compute_global_descriptors(bust)
    _, bust_vals = compute_local_descriptors(bust, len(bust.vertices), 10)

    plot_histogram('bust', 10, (3, 2), **bust_vals)


    # glasses_global = compute_global_descriptors(glasses)
    _, glasses_local = compute_local_descriptors(glasses, len(glasses.vertices), 10)
    plot_histogram('glasses', 10, **glasses_local)


    # print(bust_global)
    # print(glasses_global)

    # for i in bust_local.keys():
    #     obj = bust_local[i]
    #     mn, mx = hist_ranges[i]
    #     plot_histogram('bust', 10, mn, mx, **{i: obj})

    # for j in glasses_local.keys():
    #     obj = glasses_local[j]
    #     mn, mx = hist_ranges[j]
    #     plot_histogram('glasses', 10, mn, mx, **{j: obj})

    # meshes = read_dataset(dataset=dataset, n_meshes=10)
    # mesh_normalization(meshes.values())
    # filter_meshes(dataset)
    # for mesh in meshes.values():
    #     compute_local_descriptors(mesh, len(mesh.vertices), 10)
    #     compute_global_descriptors(mesh)
    #     draw_mesh(mesh, draw_unit_cube=True)
    # draw_meshes(list(meshes.values()), draw_unit_cube=True)
