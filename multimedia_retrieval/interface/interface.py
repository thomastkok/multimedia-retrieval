import PySimpleGUI as gui
from multimedia_retrieval.matching.matching import query_shape


def create_interface():
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
            dataset = values[0]
            mesh = values[1]
            shapes = query_shape(mesh, dataset)
        print('You entered', values)

    window.close()
