import open3d


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
