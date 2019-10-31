import matplotlib.pyplot as plt
import numpy as np
from sklearn import metrics

from .helpers import get_labels, plot_roc_curve, get_auc
from multimedia_retrieval.matching.matching import query_shape


def evaluate(features, paths, norm_info):
    shapes = features['labeled'].index
    labels = get_labels()
    classes = [labels[str(x)] for x in shapes]

    get_auc(classes,
            features['labeled'], paths['labeled'], norm_info['labeled'])
