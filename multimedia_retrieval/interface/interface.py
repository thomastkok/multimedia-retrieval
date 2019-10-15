import PySimpleGUI as gui

from multimedia_retrieval.matching.matching import query_shape
from multimedia_retrieval.visualization.visualization import draw_mesh
from multimedia_retrieval.datasets.datasets import read_mesh


def create_interface(features, paths):
    layout = [
        [gui.Text('Welcome to the 3D Shape Retrieval Program!')],
        [gui.Text('Select your dataset'),
         gui.InputCombo(('Princeton', 'Labeled'), size=(20, 1))],
        [gui.Text('Select your query shape:'), gui.Input(), gui.FileBrowse()],
        [gui.Button('Ok'), gui.Button('Cancel')]
    ]

    window = gui.Window('3D Shape Retrieval', layout)

    while True:
        event, values = window.read()
        if event in (None, 'Cancel'):
            break
        elif event in ('Ok'):
            dataset = values[0].lower()
            mesh = values[1]
            shapes = query_shape(mesh, features[dataset])
            for shape, dist in shapes.iteritems():
                print(f'The shape {shape} has distance {dist}.')
                draw_mesh(read_mesh(paths[dataset][shape]))

    window.close()
