import PySimpleGUI as sg

from multimedia_retrieval.matching.matching import query_shape
from multimedia_retrieval.visualization.visualization import draw_mesh
from multimedia_retrieval.datasets.datasets import read_mesh


def create_interface(features, paths, norm_info):
    """
    Creates the default interface for the app,
    and allows the user to query shapes.
    """
    sg.ChangeLookAndFeel('NeutralBlue')

    layout = [
        [sg.Text('Welcome to the 3D Shape Retrieval Program!')],
        [sg.Text('Select your dataset'),
         sg.InputCombo(('Labeled', 'Princeton'), size=(20, 1))],
        [sg.Text('Select your query shape:'), sg.Input(), sg.FileBrowse()],
        [sg.Button('Ok'), sg.Button('Cancel')]
    ]

    window = sg.Window('3D Shape Retrieval', layout)

    while True:
        event, values = window.read()
        if event in (None, 'Cancel'):
            break
        elif event in ('Ok'):
            dataset = values[0].lower()
            if dataset in features.keys():
                mesh = values[1]
                shapes = query_shape(mesh,
                                     features[dataset], norm_info[dataset])
                for shape, dist in shapes.iteritems():
                    answer = sg.PopupYesNo(
                        f'Shape {shape} has distance {dist}.'
                        'Do you want to view the shape?'
                    )
                    if answer == 'Yes':
                        draw_mesh(read_mesh(paths[dataset][shape]))
            else:
                sg.PopupError(f'Dataset {dataset} is not loaded.')

    window.close()
