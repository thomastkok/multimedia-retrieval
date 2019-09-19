import os
import sys
import numpy as np

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
        mesh_props[mesh] = properties
    return mesh_props
