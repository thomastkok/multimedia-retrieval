import os
import sys
import numpy as np
import open3d

import multimedia_retrieval.import_tools
from multimedia_retrieval.datasets.datasets import read_mesh


def get_classes(file_path, dataset):
    """
    Generates dictionary with class label for each mesh,
    and returns it.
    """
    classes = {}
    if dataset == 'princeton':
        for file in (file_path + '/classification/v1/base/test.cla',
                     file_path + '/classification/v1/base/train.cla'):
            with open(file) as f:
                lines = f.readlines()
                last_class_name = ''
                for line in lines:
                    split_line = line.split()
                    # First 0 means that it is a root class
                    if len(split_line) > 2 and split_line[1] == '0':
                        last_class_name = split_line[0]
                    elif len(split_line) == 1 and split_line[0].isdigit():
                        classes[split_line[0]] = last_class_name
    elif dataset == 'labeled':
        for root, dirs, files in os.walk(file_path, topdown=True):
            for file in files:
                if file.endswith('.off'):
                    index = file.split('.', 1)[0].replace('m', '')
                    classes[index] = os.path.basename(root)
    else:
        raise ValueError(f'Dataset {dataset} is not implemented')
    return classes


def get_mesh_properties(meshes, classes):
    """
    For each mesh given, determines a set of properties,
    and returns a dictionary with all meshes and properties.
    """
    mesh_props = {}
    for mesh_name in meshes.keys():
        properties = {}
        class_label = classes[mesh_name]
        mesh = meshes[mesh_name]
        properties['class'] = class_label
        properties['nr_faces'] = len(mesh.triangles)
        properties['nr_vertices'] = len(mesh.vertices)
        properties['face_type'] = 'triangles'  # by definition
        properties['bounding_box'] = mesh.get_axis_aligned_bounding_box()
        mesh_props[mesh_name] = properties
    return mesh_props


def translate_to_origin(mesh):
    """
    Translates the mesh,
    such that its centroid coincides with the coordinate-frame origin.
    """
    mesh.translate(-mesh.get_center())


def scale_to_unit(mesh):
    """
    Scales the mesh,
    such that it fits tightly in a unit-sized cube.

    The mesh must be located at the origin.
    """
    center = mesh.get_center()
    if center[0] > 0.001 or center[1] > 0.001 or center[2] > 0.001:
        raise ValueError(
            f'Mesh must be centered around the origin, not {center}'
        )
    factor = 0.5 / max(max(-mesh.get_min_bound()), max(mesh.get_max_bound()))
    mesh.scale(factor, center=True)


def unit_cube():
    """
    Creates and returns a unit cube, centered around the origin.
    """
    points = [[-0.5, -0.5, -0.5], [0.5, -0.5, -0.5], [-0.5, 0.5, -0.5],
              [0.5, 0.5, -0.5], [-0.5, -0.5, 0.5], [0.5, -0.5, 0.5],
              [-0.5, 0.5, 0.5], [0.5, 0.5, 0.5]]
    lines = [[0, 1], [0, 2], [1, 3], [2, 3], [4, 5], [4, 6], [5, 7], [6, 7],
             [0, 4], [1, 5], [2, 6], [3, 7]]
    colors = [[0, 0, 0] for i in range(len(lines))]
    line_set = open3d.geometry.LineSet()
    line_set.points = open3d.utility.Vector3dVector(points)
    line_set.lines = open3d.utility.Vector2iVector(lines)
    line_set.colors = open3d.utility.Vector3dVector(colors)
    return line_set


def align_to_eigenvectors(mesh):
    """
    Calculates the covariance matrix,
    and aligns the mesh to its eigenvectors.
    """
    vertices = np.asarray(mesh.vertices)
    eigenvectors = np.linalg.eigh(np.cov(vertices, rowvar=False))[1]
    mesh.vertices = open3d.utility.Vector3dVector(
                        np.stack([vertices @ eigenvectors[0],
                                  vertices @ eigenvectors[1],
                                  vertices @ eigenvectors[2]], axis=1))
    return mesh
    # return np.stack([vertices @ eigenvectors[0],
    #                  vertices @ eigenvectors[1],
    #                  vertices @ eigenvectors[2]], axis=1)


def flip_to_moment(mesh):
    centroid = mesh.get_center()
    print(centroid)
    return mesh
