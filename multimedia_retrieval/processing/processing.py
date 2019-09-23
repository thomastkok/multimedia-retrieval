import csv

from multimedia_retrieval.processing.helpers import (get_classes,
                                                     get_mesh_properties,
                                                     translate_to_origin,
                                                     scale_to_unit)

import multimedia_retrieval.import_tools
from multimedia_retrieval.datasets.datasets import read_dataset


def filter_meshes(dataset, file_path=None, n_meshes=None, output_file=None):
    """
    Checks all (or n) shapes in the given dataset,
    and outputs a set of properties for each shape.
    """
    if dataset == 'princeton':
        if not file_path:
            file_path = '../benchmark'
    elif dataset == 'labeled':
        if not file_path:
            file_path = '../LabeledDB_new'
    else:
        raise ValueError(f'Dataset {dataset} is not implemented')
    classes = get_classes(file_path, dataset)
    meshes = read_dataset(dataset, file_path, n_meshes)
    mesh_properties = get_mesh_properties(meshes, classes)
    if output_file and not output_file.endswith('.csv'):
        raise ValueError(f'Output file ({output_file}) should end with .csv')
    elif output_file:
        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=',')

            writer.writerow(['Mesh', 'Class', 'Number of faces',
                             'Number of vertices', 'Type of faces',
                             'Bounding box'])
            for mesh in mesh_properties.keys():
                row = [mesh]
                properties = ['class', 'nr_faces', 'nr_vertices',
                              'face_type', 'bounding_box']
                m_properties = mesh_properties[mesh]
                for prop in properties:
                    row.append(m_properties[prop])
                writer.writerow(row)
    else:
        for mesh in mesh_properties.keys():
            print(f'The properties for mesh {mesh}:')
            print(str(mesh_properties[mesh]))


def normalization(meshes):
    for mesh in meshes:
        translate_to_origin(mesh)
        scale_to_unit(mesh)
