import open3d
import trimesh
import os


def get_classes(file_path, dataset):
    """
    Generates dictionary with class label for each mesh,
    and returns it.
    """
    classes = {}
    if dataset == 'princeton':
        for file in (file_path + '/classification/v1/base/test.cla',
                     file_path + '/classification/v1/base/train.cla'):
            with open(file) as f:
                lines = f.readlines()
                last_class_name = ''
                for line in lines:
                    split_line = line.split()
                    # First 0 means that it is a root class
                    if len(split_line) > 2 and split_line[1] == '0':
                        last_class_name = split_line[0]
                    elif len(split_line) == 1 and split_line[0].isdigit():
                        classes[split_line[0]] = last_class_name
    elif dataset == 'labeled':
        for root, dirs, files in os.walk(file_path, topdown=True):
            for file in files:
                if file.endswith('.off'):
                    index = file.split('.', 1)[0].replace('m', '')
                    classes[index] = os.path.basename(root)
    else:
        raise ValueError(f'Dataset {dataset} is not implemented')
    return classes