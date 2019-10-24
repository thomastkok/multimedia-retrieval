import os


def get_labels():
    """
    Generates dictionary with class label for each mesh,
    and returns it.
    """
    file_path = '../LabeledDB_new'
    classes = {}
    for root, dirs, files in os.walk(file_path, topdown=True):
        for file in files:
            if file.endswith('.off'):
                index = file.split('.', 1)[0].replace('m', '')
                classes[index] = os.path.basename(root)
    return classes
