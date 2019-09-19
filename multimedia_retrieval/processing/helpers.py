import os


def get_class_name(file_name, dataset_name):
    # Dictionary that says which file belongs to which class for the dataset.
    files_classes = {}
    if dataset_name == 'princeton':
        with open(file_name) as f:
            lines = f.readlines()
            last_class_name = ''
            for line in lines:
                split_line = line.split()
                # First 0 means that it is a root class.
                if len(split_line) > 2 and split_line[1] == '0':
                    last_class_name = split_line[0]
                elif len(split_line) == 1:
                    if is_int(split_line[0]):
                        files_classes[split_line[0]] = last_class_name
        return files_classes


def get_mesh_properties():
    for root, dirs, files in os.walk('../benchmark', topdown=True):
        # print('root', root)
        # print('dirs', dirs)
        # print('files', files)      
        if files:
            for elem in files:
                if elem.endswith('.off'):
                    # read mesh
                    # get some properties from the mesh object
                    # create dict entry for each mesh with stats/properties
                    # add class to same dict entry
                    stripped_name = elem.split('.', 1)[0].replace('m', '')
                    class_label = files_classes[stripped_name]


def is_int(input):
    try:
        num = int(input)
    except ValueError:
        return False
    return True


file_path = '/home/ruben/Desktop/benchmark/classification/v1/base/'
get_class_name(file_path + 'test.cla', 'princeton')
# get_class_name(file_path + 'train.cla', 'princeton')
