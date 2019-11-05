import os

import open3d
import trimesh


def mesh_to_trimesh(mesh):
    """
    Converts a mesh object to a trimesh.
    """
    open3d.io.write_triangle_mesh("temp.ply", mesh)
    tri_mesh = trimesh.load_mesh("temp.ply")
    os.remove("temp.ply")
    return tri_mesh


def trimesh_to_mesh(tri_mesh):
    """
    Computes a trimesh object to a mesh object.
    """
    trimesh.exchange.export.export_mesh(tri_mesh, 'temp.ply', 'ply')
    mesh = open3d.io.read_triangle_mesh('temp.ply')
    os.remove("temp.ply")
    return mesh
