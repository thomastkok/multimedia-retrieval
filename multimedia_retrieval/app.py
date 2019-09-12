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


# from https://stackoverflow.com/questions/31129968/off-files-on-python
def read_off(file_path):
    with open(file_path, 'r') as off_file:
        if 'OFF' != off_file.readline().strip():
            raise('Not a valid OFF header')
        n_verts, n_faces, n_edges = tuple(
            [int(s) for s in off_file.readline().strip().split(' ')])
        verts = [[float(s) for s in off_file.readline().strip().split(' ')]
                 for i_vert in range(n_verts)]
        faces = [[int(s) for s in off_file.readline().strip().split(' ')][1:]
                 for i_face in range(n_faces)]
        return verts, faces
