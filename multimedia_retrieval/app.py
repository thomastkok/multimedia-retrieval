import open3d

from .datasets.datasets import read_dataset, read_mesh
from .descriptors.descriptors import (compute_global_descriptors,
                                      compute_local_descriptors)

from .descriptors.helpers import (get_hist_ranges)


from .filter.filter import filter_meshes, refine_outlier
from .normalization.normalization import (feature_normalization,
                                          mesh_normalization)
from .visualization.visualization import draw_mesh, draw_meshes

from .histograms.histograms import plot_histogram


def run():

    hist_ranges = get_hist_ranges()

    dataset = input('Please specify the dataset (princeton/labeled): ')
    if not dataset:
        dataset = 'labeled'

    bust = read_mesh('/home/ruben/Desktop/LabeledDB_new/Bust/310.off')
    glasses = read_mesh('/home/ruben/Desktop/LabeledDB_new/Glasses/49.off')

    meshes = [bust, glasses]
    mesh_normalization(meshes)

    bust_global = compute_global_descriptors(bust)
    bust_local = compute_local_descriptors(bust, len(bust.vertices), 10)

    glass_global = compute_global_descriptors(glasses)
    glass_local = compute_local_descriptors(glasses, len(glasses.vertices), 10)

    for i in bust_local.keys():
        obj = bust_local[i]
        mn, mx = hist_ranges[i]
        plot_histogram('bust', 10, mn, mx, **{i: obj})

    for j in glass_local.keys():
        obj, mn, mx = glass_local[j]
        print({j: (max(obj), max(obj) < mx)})
        plot_histogram('glass', 10, mn, mx, **{j: obj})

    # meshes = read_dataset(dataset=dataset, n_meshes=10)
    # mesh_normalization(meshes.values())
    # filter_meshes(dataset)
    # for mesh in meshes.values():
    #     compute_local_descriptors(mesh, len(mesh.vertices), 10)
    #     compute_global_descriptors(mesh)
    #     draw_mesh(mesh, draw_unit_cube=True)
    # draw_meshes(list(meshes.values()), draw_unit_cube=True)
