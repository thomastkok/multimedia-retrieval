import PySimpleGUI as sg

from multimedia_retrieval.matching.matching import query_shape
from multimedia_retrieval.visualization.visualization import draw_mesh
from multimedia_retrieval.datasets.datasets import read_mesh
from multimedia_retrieval.ann.ann import approximate_nn


def create_interface(features, paths, norm_info):
    """
    Creates the default interface for the app,
    and allows the user to query shapes.
    """
    sg.ChangeLookAndFeel('NeutralBlue')

    layout = [
        [sg.Text('Welcome to the 3D Shape Retrieval Program!')],
        [sg.Text('Select your dataset'),
         sg.InputCombo(('Labeled', 'Princeton'), size=(20, 1),
                       key='dataset')],
        [sg.Text('Select your query method:'),
         sg.Radio('By id', group_id="RADIO0", enable_events=True,
                  key='by_id', default=True),
         sg.Radio('By mesh', group_id="RADIO0", enable_events=True,
                  key='by_mesh')],
        [sg.Text('Input the id of your query shape:'),
         sg.Input(key='query_id')],
        [sg.Text('Select your query shape:'), sg.Input(key='query_shape'),
         sg.FileBrowse()],
        [sg.Text('Select your distance calculation method:'),
         sg.Radio('Regular', group_id="RADIO1", enable_events=True,
                  key='regular', default=True),
         sg.Radio('Ann', enable_events=True, group_id="RADIO1", key='ann')],
        [sg.Text('Input k (the number of returned shapes):'),
         sg.Slider(range=(1, 20), orientation='horizontal',
                   default_value=3, key='k')],
        [sg.Button('Ok'), sg.Button('Cancel')]
    ]

    window = sg.Window('3D Shape Retrieval', layout)

    while True:
        print(f'Values found in window are {window.read()}')
        event, values = window.read()

        if event in (None, 'Cancel'):
            break
        elif event in ('Ok'):
            dataset = values['dataset'].lower()
            if values['by_id'] and (not values['query_id'].isdigit() or not
                                    (0 < int(values['query_id']) <= 380)):
                sg.PopupError(f'Query ID must be a digit between 1 and 380, \
                                not {values["query_id"]}')
            if dataset in features.keys():
                mesh = values['query_id'] if values['by_id'] else values['query_shape']

                if values['regular']:
                    shapes = query_shape(
                        mesh, features[dataset], norm_info[dataset],
                        k=int(values['k']))
                elif values['ann']:
                    shapes = approximate_nn(
                        mesh, features[dataset], 100, 5,
                        int(values['k']), norm_info[dataset])

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
