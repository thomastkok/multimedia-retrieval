import os
import sys
import numpy as np

import multimedia_retrieval.import_tools
from multimedia_retrieval.datasets.datasets import read_mesh


def get_class_name(file, dataset):
    # Dictionary that says which file belongs to which class for the dataset.
    classes = {}
    if dataset == 'princeton':
        with open(file) as f:
            lines = f.readlines()
            last_class_name = ''
            for line in lines:
                split_line = line.split()
                # First 0 means that it is a root class.
                if len(split_line) > 2 and split_line[1] == '0':
                    last_class_name = split_line[0]
                elif len(split_line) == 1 and split_line[0].isdigit():
                    classes[split_line[0]] = last_class_name
        return classes
    else:
        raise ValueError(f'Dataset {dataset} not implemented yet')


def get_mesh_properties(meshes, classes):
    mesh_props = {}
    for mesh_name in meshes.keys():
        properties = {}
        class_label = classes[mesh_name]
        mesh = meshes[mesh_name]
        properties['class'] = class_label
        properties['nr_faces'] = len(mesh.triangles)
        properties['nr_vertices'] = len(mesh.vertices)
        properties['faces_type'] = 'triangles'  # by definition
        properties['bounding_box'] = mesh.get_axis_aligned_bounding_box()
        mesh_props[mesh] = properties
    return mesh_props
