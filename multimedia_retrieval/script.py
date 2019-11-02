from multimedia_retrieval.datasets.datasets import read_mesh
from multimedia_retrieval.visualization.visualization import draw_mesh
from multimedia_retrieval.normalization.mesh_norm import (
    translate_to_origin, align_to_eigenvectors,
    flip_mesh, scale_to_unit
)
import open3d

mesh = read_mesh('C:\\Users\\Thomas\\Documents\\mr\\LabeledDB_new\\Human\\2.off')
mesh.translate((-1, 0.2, 0.45))
mesh.scale(1.3)
mesh.rotate((260, 215, 188), type=open3d.geometry.RotationType.AxisAngle)

draw_mesh(mesh, draw_coordinate_frame=True)
translate_to_origin(mesh)
draw_mesh(mesh, draw_coordinate_frame=True)
align_to_eigenvectors(mesh)
draw_mesh(mesh, draw_coordinate_frame=True)
flip_mesh(mesh)
draw_mesh(mesh, draw_coordinate_frame=True)
scale_to_unit(mesh)
draw_mesh(mesh, draw_coordinate_frame=True)
