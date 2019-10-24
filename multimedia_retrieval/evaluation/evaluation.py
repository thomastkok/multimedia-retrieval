import matplotlib.pyplot as plt
import numpy as np
from sklearn import metrics

from .helpers import get_labels
from multimedia_retrieval.matching.matching import query_shape


def evaluate(features, paths, norm_info):
    mesh = 'C:\\Users\\Thomas\\Documents\\mr\\LabeledDB_new\\Airplane\\61.off'
    shapes = query_shape(mesh, features['labeled'], norm_info['labeled'],
                         k=None)

    labels = get_labels()

    classes = [labels[str(x)] for x in shapes.index]
    distances = [-x for x in shapes]
    true_class = labels['61']

    plot_roc_curve(classes, distances, true_class)


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
