import open3d
import numpy as np
from .helpers import unit_cube


def draw_mesh(mesh, draw_unit_cube=False, draw_coordinate_frame=False,
              draw_eigenvectors=False):
    """Draws a single given mesh."""

    shapes = [mesh]

    # The x, y, z axis will be rendered as red, green, and blue arrows
    #  respectively.
    if draw_coordinate_frame:
        mesh_frame = open3d.geometry.TriangleMesh.create_coordinate_frame(
            origin=[0, 0, 0])
        shapes.append(mesh_frame)

    if draw_eigenvectors:
        eigenvectors = np.linalg.eigh(np.cov(mesh.vertices, rowvar=False))[1]
        points = [[0, 0, 0]]

        points.append(eigenvectors[:, 0])
        points.append(eigenvectors[:, 1])
        points.append(eigenvectors[:, 2])

        lines = [[0, 1], [0, 2], [0, 3]]

        #  smallest is black, middle cyan, largest magenta.
        colors = [[0, 0, 0], [0, 1, 1], [1, 0, 1]]

        line_set = open3d.geometry.LineSet()

        line_set.lines = open3d.utility.Vector2iVector(lines)
        line_set.points = open3d.utility.Vector3dVector(points)
        line_set.colors = open3d.utility.Vector3dVector(colors)

        shapes.append(line_set)

    open3d.visualization.draw_geometries(shapes)


def draw_meshes(meshes, draw_unit_cube=False, draw_coordinate_frame=False):
    """Draws a list of given meshes."""
    shapes = meshes
    shapes.append(mesh_frame)

    if draw_unit_cube:
        shapes.append(unit_cube())
    open3d.visualization.draw_geometries(shapes)
