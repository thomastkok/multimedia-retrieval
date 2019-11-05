import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sn
from sklearn import metrics

from multimedia_retrieval.matching.distances import compare

from .helpers import get_labels, print_auc


def evaluate(features, paths, norm_info, dist_df):
    """Evalutes the given feature set, and distance matrix."""
    shapes = features['labeled'].index
    labels = get_labels()
    classes = [labels[str(x)] for x in shapes]

    print_auc(classes, dist_df,
              features['labeled'], paths['labeled'], norm_info['labeled'])


def plot_conf_matrix(features, dist_df):
    """Plots a confusion matrix, given a distance matrix."""
    features = features['labeled']
    shapes = features.index
    labels = get_labels()
    classes = [labels[str(x)] for x in shapes]

    pred = []
    for s in shapes:
        pred.append(
            dist_df.loc[s, :].sort_values().index[1]
        )
    pred = [labels[str(x)] for x in pred]

    lbl = sorted(list(set(classes)))
    conf_mat = metrics.confusion_matrix(classes, pred, lbl)
    df_cm = pd.DataFrame(conf_mat, index=lbl, columns=lbl)
    plt.figure(figsize=(10, 7))
    sn.heatmap(df_cm, annot=True)
    plt.ylim(plt.ylim()[0] + 0.5, plt.ylim()[1] - 0.5)
    plt.show()


def get_dist_mat(features=None, cache=True):
    """Either reads a distance matrix from cache, or generates one."""
    if cache:
        dist_df = pd.read_csv('./cache/dist_labeled.csv', sep='#', index_col=0)
    else:
        dist_df = pd.DataFrame(np.zeros(shape=(380, 380)),
                               columns=features.index)
        dist_df.index = features.index

        print('Creating distance matrix.')

        for i in features.index:
            for j in features.index:
                if i < j:
                    dist = compare(features.loc[i, :], features.loc[j, :])
                    dist_df.loc[i, j] = dist
                    dist_df.loc[j, i] = dist

        print('Distance matrix created.')

        dist_df.to_csv(f'./cache/dist_labeled.csv', sep='#', index=True)
    return dist_df
