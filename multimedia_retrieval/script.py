from multimedia_retrieval.datasets.datasets import read_mesh
from multimedia_retrieval.visualization.visualization import draw_mesh

from multimedia_retrieval.matching.matching import query_shape
from multimedia_retrieval.ann.ann import approximate_nn


from multimedia_retrieval.datasets.datasets import read_cache
from multimedia_retrieval.evaluation.evaluation import get_labels

import open3d
import matplotlib.pyplot as plt
import numpy as np

query_mesh = "/home/ruben/Desktop/LabeledDB_new/Plier/207.off"
features, paths, norm_info = read_cache()

top_ks = [10, 100]
labels = get_labels()
metrics = ['euclidean', 'angular', 'manhattan', 'dot']
colors = ['k', 'r', 'g', 'b']


cmap = plt.cm.jet

# shapes_regular = query_shape(
#     query_mesh, features['labeled'], norm_info['labeled'], top_k)

fig, axs = plt.subplots(nrows=4, ncols=2)

handles, labs = [], []


for midx, metric in enumerate(metrics):
    for idx, top_k in enumerate(top_ks):
        shapes_ann = approximate_nn(
            query_mesh, features['labeled'], 10000, 100000, top_k, norm_info['labeled'], metric)
        x, y = [], []
        for shape, dist in shapes_ann.iteritems():
            x.append(dist)
            y.append(labels[f'{shape}'])

        handle, = axs[midx, idx].plot(x, y, "o-", c=colors[midx], alpha=0.6, label=metric)
        handles.append(handle)
        labs.append(metric)


handle_list, label_list = [], []
for handle, label in zip(handles, labs):
    if label not in label_list:
        handle_list.append(handle)
        label_list.append(label)


fig.legend(handles=handle_list, labels=label_list, loc='lower center')

plt.suptitle(f'Comparison of top-10 and top-100 between ANN metrics')
fig.text(0.5, 0.90, 'Distances', ha='center', va='center')
fig.text(0.06, 0.5, 'Classes', ha='center', va='center', rotation='vertical')

plt.show()
