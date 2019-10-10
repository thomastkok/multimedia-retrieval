import open3d
from .helpers import unit_cube


def draw_mesh(mesh, draw_unit_cube=False):
    """Draws a single given mesh."""
    draw_meshes([mesh], unit_cube)


def draw_meshes(meshes, draw_unit_cube=False):
    """Draws a list of given meshes."""
    shapes = meshes
    if draw_unit_cube:
        shapes.append(unit_cube())
    open3d.visualization.draw_geometries(shapes)
