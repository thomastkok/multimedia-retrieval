from multimedia_retrieval.filter.helpers import (
    get_classes, output_filter, fix_outliers,
    refine_outliers, get_average_obj, get_mesh_properties,
    get_stat_property_names, get_stats,
    mesh_to_trimesh, trimesh_to_mesh
)
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
    mesh_stats = get_stats(mesh_properties)

    avg_faces = int(mesh_stats['avg']['nr_faces'])
    avg_vertices = int(mesh_stats['avg']['nr_vertices'])

    closest_obj, closest_id = get_average_obj(
                                avg_vertices, avg_faces,
                                mesh_properties
                              )

    print(closest_obj)
    print(closest_id)

    fix_outliers(meshes, avg_faces, dataset, 1.3)

    mesh_properties = get_mesh_properties(meshes, classes)
    mesh_stats = get_stats(mesh_properties)

    output_filter(output_file, mesh_properties, mesh_stats)
