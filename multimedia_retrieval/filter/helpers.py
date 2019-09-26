import numpy as np
import sys
import open3d
import trimesh
import statistics
import csv


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


def output_filter(output_file, mesh_properties, mesh_stats):
    if output_file and not output_file.endswith('.csv'):
        raise ValueError(f'Output file ({output_file}) should end with .csv')
    elif output_file:
        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=',')

            properties = ['class'] + get_stat_property_names()
            writer.writerow(['Mesh', 'Class', 'Number of faces',
                             'Number of vertices', 'Type of faces',
                             'Bounding box volume', 'Centroid',
                             'Normalized number of faces',
                             'Normalized number of vertices',
                             'Normalized bounding box volume',
                             'Normalized centroid'])
            for mesh in mesh_properties.keys():
                row = [mesh]
                m_properties = mesh_properties[mesh]
                for prop in properties:
                    row.append(m_properties[prop])
                writer.writerow(row)

            writer.writerow([])

            for stat_key in mesh_stats.keys():
                row = [stat_key]
                stats = mesh_stats[stat_key]
                for prop in properties:
                    has_key = stats.get(prop)
                    if has_key is None:
                        row.append(-1)
                    else:
                        row.append(has_key)

                writer.writerow(row)
    else:
        for mesh in mesh_properties.keys():
            print(f'The properties for mesh {mesh}:')
            print(str(mesh_properties[mesh]))


def get_stat_property_names():
    return ['nr_faces', 'nr_vertices',
            'bounding_box_vol', 'centroid']


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
        properties['bounding_box_vol'] = \
            mesh.get_axis_aligned_bounding_box().volume()
        properties['centroid'] = mesh.get_center()
        mesh_props[mesh_name] = properties

    return mesh_props


def get_stats(mesh_props):
    # Get min, max and avg
    mesh_stats = {}
    mins = {}
    maxs = {}
    means = {}
    for prop in get_stat_property_names():
        numbers = [mesh_props[key][prop] for key in mesh_props]
        if type(numbers[0]) is np.ndarray:
            mean = np.mean(numbers, axis=0)
            mn = np.min(numbers, axis=0)
            mx = np.max(numbers, axis=0)
            mins[prop] = mn
            maxs[prop] = mx
            means[prop] = mean
        else:
            mean = statistics.mean(numbers)
            mn = min(numbers)
            mx = max(numbers)
            mins[prop] = mn
            maxs[prop] = mx
            means[prop] = mean

    mesh_stats['min'] = mins
    mesh_stats['max'] = maxs
    mesh_stats['avg'] = means
    return mesh_stats


def refine_outliers(mesh, face_average, lb, ub, is_small):
    """
    Refines the outliers,
    by dividing the triangles or merging them using trimesh.
    """
    if is_small:
        while len(mesh.triangles) < lb:
            mesh = mesh.subdivide_midpoint()

        if len(mesh.triangles) > ub:
            mesh = mesh.simplify_quadric_decimation(face_average)
    else:
        mesh = mesh.simplify_quadric_decimation(face_average)

    # Some post-processing.
    # Removing faces which do not have 3 unique vertex indices.
    # Only removes a small portion of triangles and vertices.

    mesh = mesh.remove_degenerate_triangles()
    mesh = mesh.remove_duplicated_triangles()
    mesh = mesh.remove_duplicated_vertices()
    mesh = mesh.remove_unreferenced_vertices()

    return mesh
