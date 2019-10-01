import open3d
import trimesh
import os


def mesh_to_trimesh(mesh):
    open3d.io.write_triangle_mesh("temp.ply", mesh)
    tri_mesh = trimesh.load_mesh("temp.ply")
    os.remove("temp.ply")
    return tri_mesh


def trimesh_to_mesh(tri_mesh):
    trimesh.exchange.export.export_mesh(tri_mesh, 'temp.ply', 'ply')
    mesh = open3d.io.read_triangle_mesh('temp.ply')
    os.remove("temp.ply")
    return mesh
