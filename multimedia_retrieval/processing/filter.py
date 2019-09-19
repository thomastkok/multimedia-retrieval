from multimedia_retrieval.processing.helpers import (get_class_name,
                                                     get_mesh_properties)

import multimedia_retrieval.import_tools
from multimedia_retrieval.datasets.datasets import read_dataset


def filter_meshes(dataset, file_path=None, n_meshes=None):
    if dataset == 'princeton':
        if not file_path:
            file_path = file_path = '../benchmark'
        classes = {
            **get_class_name(file_path + '/classification/v1/base/test.cla', dataset),
            **get_class_name(file_path + '/classification/v1/base/train.cla', dataset)
        }
    else:
        raise ValueError(f'Dataset {dataset} not implemented yet')
    meshes = read_dataset(dataset, file_path, n_meshes)
    mesh_properties = get_mesh_properties(meshes, classes)
    for mesh in mesh_properties.keys():
        print(f'The properties for mesh {mesh}:')
        print(str(mesh_properties[mesh]))
