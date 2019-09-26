import numpy as np
import sys
import open3d
import trimesh
import statistics

import multimedia_retrieval.import_tools
from multimedia_retrieval.datasets.datasets import read_mesh


# TODO:  average face area.
def get_stat_property_names():
    return ['nr_faces', 'nr_vertices',
            'bounding_box_vol', 'centroid',
            'nr_faces_n', 'nr_vertices_n',
            'bounding_box_vol_n', 'centroid_n']


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
        # properties['bounding_box_'] = np.asarray(
        #     mesh.get_axis_aligned_bounding_box().get_box_points())
        mesh_props[mesh_name] = properties

    normalization_tool(meshes)
    for mesh_name in meshes.keys():
        properties = {}
        mesh = meshes[mesh_name]
        properties['nr_faces_n'] = len(mesh.triangles)
        properties['nr_vertices_n'] = len(mesh.vertices)
        properties['bounding_box_vol_n'] = \
            mesh.get_axis_aligned_bounding_box().volume()
        properties['centroid_n'] = mesh.get_center()
        # properties['bounding_box_n'] = np.asarray(
        #     mesh.get_axis_aligned_bounding_box().get_box_points())
        mesh_props[mesh_name].update(properties)

    return mesh_props


def get_average_obj(avg_vertices, avg_faces, mesh_props):

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


def normalization_tool(meshes):
    for mesh in meshes.values():
        translate_to_origin(mesh)
        scale_to_unit(mesh)


def mesh_to_trimesh(mesh):
    open3d.io.write_triangle_mesh("temp.ply", mesh)
    tri_mesh = trimesh.load_mesh("temp.ply")
    return tri_mesh


def trimesh_to_mesh(tri_mesh):
    trimesh.exchange.export.export_mesh(tri_mesh, 'temp.ply', 'ply')
    mesh = open3d.io.read_triangle_mesh('temp.ply')
    return mesh


def draw_mesh(mesh):
    open3d.visualization.draw_geometries([mesh])


def refine_outliers(mesh, face_average, lb, ub, is_small, dataset):
    """
    Refines the outliers,
    by dividing the triangles or merging them using trimesh.
    """

    # draw_mesh(mesh)

    if is_small:
        rnd = 0
        while len(mesh.triangles) < lb:
            mesh = mesh.subdivide_midpoint()

        if len(mesh.triangles) > ub:
            mesh = mesh.simplify_quadric_decimation(face_average)
    else:
        mesh = mesh.simplify_quadric_decimation(face_average)

        # print('After decimation', len(mesh.vertices))
        # print('After decimation', len(mesh.triangles))

    # Some post-processing.
    # Removing faces which do not have 3 unique vertex indices.
    # Only removes a small portion of triangles and vertices.

    mesh = mesh.remove_degenerate_triangles()
    mesh = mesh.remove_duplicated_triangles()
    mesh = mesh.remove_duplicated_vertices()
    mesh = mesh.remove_unreferenced_vertices()

    # draw_mesh(mesh)

    return mesh
