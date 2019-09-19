from multimedia_retrieval.processing.helpers import (get_classes,
                                                     get_mesh_properties)

import multimedia_retrieval.import_tools
from multimedia_retrieval.datasets.datasets import read_dataset


def filter_meshes(dataset, file_path=None, n_meshes=None):
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
        raise ValueError(f'Dataset {dataset} not implemented yet')
    classes = get_classes(file_path, dataset)
    meshes = read_dataset(dataset, file_path, n_meshes)
    mesh_properties = get_mesh_properties(meshes, classes)
    for mesh in mesh_properties.keys():
        print(f'The properties for mesh {mesh}:')
        print(str(mesh_properties[mesh]))
