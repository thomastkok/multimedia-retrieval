import os

import open3d
import pandas as pd
import trimesh

from multimedia_retrieval.descriptors.descriptors import (
    compute_global_descriptors, compute_local_descriptors)
from multimedia_retrieval.normalization.normalization import mesh_normalization
from .helpers import hist_convert


def read_mesh(file_path):
    """
    Reads the mesh file located at the specified file path,
    and returns the mesh as open3d object.

    Args:
        file_path (str): The file path of the mesh, to be read.

    Returns:
        TriangleMesh: The mesh as an open3d object.

    """
    off = False
    if file_path.endswith('.off'):
        mesh = trimesh.load_mesh(file_path)
        trimesh.exchange.export.export_mesh(mesh, './temp.ply', 'ply')
        file_path = './temp.ply'
        off = True
    if file_path.endswith('.ply'):
        mesh = open3d.io.read_triangle_mesh(file_path)
    else:
        raise ValueError('Input file must be either .OFF or .PLY format')
    if off:
        os.remove('./temp.ply')
    return mesh


def read_dataset(dataset, file_path=None, n_meshes=None, features=False):
    """
    Reads either the princeton or labeled dataset,
    located at the specified file path,
    and returns a dictionary of n meshes.

    Args:
        dataset (str): The name of the dataset to be read, must
            be either 'princeton' or 'labeled'.
        file_path (str): The location of the dataset.
        n_meshes (int): The number of meshes to be read.

    Returns:
        dict{int: TriangleMesh}: Returns a dictionary of all meshes.

    """
    if n_meshes:
        total = {'princeton': 1814, 'labeled': 380}
        step = total[dataset] // n_meshes
        since_last_step = -1
    meshes = {}
    paths = {}
    n_meshes_loaded = 0
    if dataset == 'princeton':
        if not file_path:
            file_path = '../benchmark'
        file_path = file_path + '/db'
    elif dataset == 'labeled':
        if not file_path:
            file_path = '../LabeledDB_new'
    else:
        raise ValueError(f'{dataset} is not a known dataset, \
                         should be either "princeton" or "labeled"')
    for root, dirs, files in os.walk(file_path, topdown=True):
        if files:
            for file in files:
                if file.endswith('.off'):
                    if n_meshes:
                        since_last_step += 1
                        if since_last_step == step:
                            since_last_step = 0
                        if since_last_step > 0:
                            continue
                    mesh = read_mesh(root + '/' + file)
                    index = file.split('.', 1)[0].replace('m', '')
                    if features:
                        mesh_normalization(mesh)
                        meshes[index] = pd.concat([
                            compute_global_descriptors(mesh),
                            compute_local_descriptors(mesh, 100, 10),
                        ])
                        paths[index] = root + '/' + file
                    else:
                        meshes[index] = mesh
                    if n_meshes:
                        n_meshes_loaded = n_meshes_loaded + 1
                        if n_meshes_loaded >= n_meshes:
                            if features:
                                return (pd.DataFrame(meshes).T,
                                        pd.Series(paths,
                                        name='paths').rename_axis('mesh'))
                            return pd.Series(meshes)
    if features:
        return (pd.DataFrame(meshes).T,
                pd.Series(paths, name='paths').rename_axis('mesh'))
    return pd.Series(meshes)


def write_cache(features, paths, norm_info):
    for dataset in ('princeton', 'labeled'):
        features[dataset].to_csv(f'./cache/features_{dataset}.csv', sep='#',
                                 index=True)
        paths[dataset].to_csv(f'./cache/paths_{dataset}.csv', header=True)
        norm_info[dataset].to_csv(f'./cache/norm_info_{dataset}.csv')


def read_cache():
    features = {}
    paths = {}
    norm_info = {}
    for dataset in ('princeton', 'labeled'):
        features[dataset] = pd.read_csv(f'./cache/features_{dataset}.csv',
                                        sep='#', index_col=0,
                                        converters={
                                            'A3': hist_convert,
                                            'D1': hist_convert,
                                            'D2': hist_convert,
                                            'D3': hist_convert,
                                            'D4': hist_convert
                                        })
        paths[dataset] = pd.read_csv(f'./cache/paths_{dataset}.csv',
                                     squeeze=True, index_col=0, header=0)
        norm_info[dataset] = pd.read_csv(f'./cache/norm_info_{dataset}.csv',
                                         index_col=0)
    return features, paths, norm_info
