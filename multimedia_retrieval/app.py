import open3d

import multimedia_retrieval.datasets.datasets as datasets


def run():
    file_path = input('Please input the file path of the dataset:  ')
    dataset = input('Please specify the dataset (princeton/labeled): ')
    meshes = datasets.read_dataset(dataset, file_path, 10)
    print(meshes)
    file_path = input('Please input the file path of the .OFF or .PLY file: ')
    mesh = datasets.read_mesh(file_path)
    open3d.visualization.draw_geometries([mesh])
