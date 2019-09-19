def filter(dataset='princeton', file_path='../benchmark/classification/v1/base/'):
    files_classes = {**get_class_name(file_path + 'test.cla', dataset),
                     **get_class_name(file_path + 'train.cla', dataset)}
    get_mesh_properties(files_classes)
