import os

import open3d
import trimesh


def read_mesh(file_path):
    """
    Reads the mesh file located at the specified file path,
    and returns the mesh as open3d object.
    """
    off = False
    original_file_path = file_path
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


def read_dataset(dataset, file_path=None, n_meshes=None):
    """
    Reads either the princeton or labeled dataset,
    located at the specified file path,
    and returns a dictionary of n meshes.
    """
    meshes = {}
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
                    mesh = read_mesh(root + '/' + file)
                    index = file.split('.', 1)[0].replace('m', '')
                    meshes[index] = mesh
                    if n_meshes:
                        n_meshes_loaded = n_meshes_loaded + 1
                        if n_meshes_loaded >= n_meshes:
                            return meshes
    return meshes
