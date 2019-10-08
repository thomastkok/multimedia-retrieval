import open3d
from .helpers import unit_cube


def draw_mesh(mesh, draw_unit_cube=False):
    draw_meshes([mesh], draw_unit_cube)


def draw_meshes(meshes, draw_unit_cube=False):
    shapes = meshes
    if draw_unit_cube:
        shapes.append(unit_cube())
    open3d.visualization.draw_geometries(shapes)
