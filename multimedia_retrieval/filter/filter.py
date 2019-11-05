import sys

from multimedia_retrieval.datasets.datasets import read_dataset

from .helpers import (get_classes, get_mesh_properties, get_stats,
                      output_filter, refine_outlier)


def filter_meshes(dataset, file_path=None, n_meshes=None,
                  meshes=None, output_file=None):
    """
    Checks all (or n) shapes in the given dataset,
    and outputs a set of properties for each shape.

    Args:
        dataset (str): The name of the dataset to be read, must
            be either 'princeton' or 'labeled'.
        file_path (str): file_path (str): The file path of the dataset,
            to be read.
        n_meshes (int): The number of meshes to be read. If None, read all.
        meshes (dict{int: TriangleMesh}): The meshes to be filtered,
            if already read.
        output_file (str): The path of the file to write the output to,
            if not writing to console.

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
    if not meshes:
        meshes = read_dataset(dataset, file_path, n_meshes)
    mesh_properties = get_mesh_properties(meshes, classes)
    mesh_stats = get_stats(mesh_properties)

    output_filter(output_file, mesh_properties, mesh_stats)


def fix_outliers(meshes, face_average, offset=1.3):
    """
    Fixes the meshes that are considered outliers.
    The mesh outliers are those that have 30% more or less vertices and faces.
    """
    lower_bound = face_average * (1/offset)
    upper_bound = face_average * offset
    for mesh_key in meshes.keys():
        mesh = meshes[mesh_key]
        if (len(mesh.triangles) < lower_bound or
                len(mesh.vertices) < lower_bound):
            mesh = refine_outlier(
                mesh, face_average, lower_bound, upper_bound, True)
        elif (len(mesh.triangles) > upper_bound or
              len(mesh.triangles) > upper_bound):
            mesh = refine_outlier(
                mesh, face_average, lower_bound, upper_bound, False)
        meshes[mesh_key] = mesh


def get_average_obj(mesh_stats, mesh_props):
    """
    Obtains the average objects found in a dataset.
    It computes the smallest distance between the vertices and faces
    With the average vertices and faces.
    The distance is computed using the Manhattan distance.
    """
    avg_faces = int(mesh_stats['avg']['nr_faces'])
    avg_vertices = int(mesh_stats['avg']['nr_vertices'])

    closest_obj = sys.maxsize
    closest_mesh_id = -1

    for mesh_key in mesh_props.keys():
        vertices = mesh_props[mesh_key]['nr_vertices']
        faces = mesh_props[mesh_key]['nr_faces']
        dist = abs(vertices - avg_vertices) + abs(faces - avg_faces)
        if dist < closest_obj:
            closest_obj = dist
            closest_mesh_id = mesh_key

    return (closest_obj, closest_mesh_id)
