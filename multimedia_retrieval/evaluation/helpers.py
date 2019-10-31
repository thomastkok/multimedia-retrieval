import os
import matplotlib.pyplot as plt
import numpy as np
from sklearn import metrics, preprocessing
from multimedia_retrieval.matching.matching import query_shape
from multimedia_retrieval.matching.distances import compare


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


def plot_roc_curve(labels, distances, true_label):
    fpr, tpr, thresholds = metrics.roc_curve(labels, distances, true_label)
    roc_auc = metrics.auc(fpr, tpr)

    plt.figure()
    lw = 2
    plt.plot(fpr, tpr, color='darkorange',
             lw=lw, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic')
    plt.legend(loc="lower right")
    plt.show()


def get_auc(classes, features, paths, norm_info):
    auc_scores = {}
    for k in set(classes):
        auc_scores[k] = []

    labels = get_labels()

    for mesh in features.index:
        shapes = query_shape(paths[mesh], features, norm_info, k=None)
        fpr, tpr, _ = metrics.roc_curve(
            [labels[str(x)] for x in shapes.index],
            [-x for x in shapes],
            labels[str(mesh)]
        )
        auc_scores[labels[str(mesh)]].append(metrics.auc(fpr, tpr))
        print(f'Processed mesh {mesh}.')

    print(auc_scores)

    for k in auc_scores.keys():
        print(f'The average for {k} is {np.mean(auc_scores[k])}')

    return auc_scores
