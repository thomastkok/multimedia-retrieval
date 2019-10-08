from .helpers import (
    output_filter, refine_outliers, get_classes,
    get_mesh_properties, get_stat_property_names, get_stats
)
from multimedia_retrieval.datasets.datasets import read_dataset
from multimedia_retrieval.mesh_conversion.helpers import (mesh_to_trimesh,
                                                          trimesh_to_mesh)


def filter_meshes(dataset, file_path=None, n_meshes=None,
                  meshes=None, output_file=None):
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
    if not meshes:
        meshes = read_dataset(dataset, file_path, n_meshes)
    mesh_properties = get_mesh_properties(meshes, classes)
    mesh_stats = get_stats(mesh_properties)

    output_filter(output_file, mesh_properties, mesh_stats)


def fix_outliers(meshes, face_average, offset=1.3):
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
