import open3d
import trimesh
import os


def run():
    file_path = input('Please input the file path of the .OFF or .PLY file:')
    off = False
    if file_path.endswith('.off'):
        mesh = trimesh.load_mesh(file_path)
        trimesh.exchange.export.export_mesh(mesh, './temp.ply', 'ply')
        print('Saved .OFF file as .PLY file')
        file_path = './temp.ply'
        off = True
    if file_path.endswith('.ply'):
        mesh = open3d.io.read_triangle_mesh(file_path)
        print(type(mesh))
        print('Read .PLY file')
    else:
        raise ValueError('Input file must be either .OFF or .PLY format')
    if off:
        os.remove('./temp.ply')
    open3d.visualization.draw_geometries([mesh])
