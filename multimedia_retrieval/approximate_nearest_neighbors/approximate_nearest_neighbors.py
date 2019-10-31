from annoy import AnnoyIndex
from nearpy import Engine
from nearpy.hashes import RandomBinaryProjections

from multimedia_retrieval.datasets.datasets import read_dataset, read_mesh
from multimedia_retrieval.matching.matching import compute_mesh_features

from ..matching.distances import compare, CustomCompare

import random
import numpy as np
import pandas as pd

# There are just two main parameters needed to tune Annoy:
# the number of trees n_trees and the number of nodes to inspect during searching search_k.

# n_trees is provided during build time and affects the build time and the index size.
#  A larger value will give more accurate results, but larger indexes.
# search_k is provided in runtime and affects the search performance.
# A larger value will give more accurate results, but will take longer time to return.


def approximate_nn(query_mesh_path, feature_db, number_trees, search_k, top_k, norm_info):

    query_mesh_features = compute_mesh_features(query_mesh_path, norm_info)
    nr_bins = 10

    query_vector = []
    for feat in query_mesh_features:
        if isinstance(feat, tuple):
            hist_vals = feat[0]
            for h_val in hist_vals:
                query_vector.append(h_val / nr_bins)
        else:
            query_vector.append(feat)

    n_rows, n_cols = feature_db.shape
    ann = AnnoyIndex(55, 'euclidean')

    ann.add_item(0, query_vector)

    for index, row in feature_db.iterrows():
        feature_vect = []
        for col_name in feature_db.columns:
            #  Its a histogram
            if isinstance(row[col_name], tuple):
                hist_vals = row[col_name][0]
                for val in hist_vals:
                    feature_vect.append(val / nr_bins)
            else:
                feature_vect.append(row[col_name])
        ann.add_item(index, feature_vect)

    ann.build(number_trees)
    # Gets the 5 nearest items that are closest to 61.

    shapes = ann.get_nns_by_item(
        0, top_k, search_k=search_k, include_distances=True)

    results = {}

    for id, dist in list(zip(shapes[0], shapes[1])):
        results[id] = dist 

    shapes = pd.Series(results).sort_values()

    return shapes


def approximate_nearpy(feature_db):
    dimension = 10
    # rbp = RandomBinaryProjections('rbp', 10)
    # engine = Engine(dimension, lshashes=[rbp], distance=CustomCompare())

    # last_row = None

    # for data_point, dp_features in feature_db.iterrows():
    #     last_row = dp_features
    #     engine.store_vector(dp_features, f'data {data_point}')

    # print(last_row)
    # query = last_row
    # N = engine.neighbours(query)
    # print(N)
