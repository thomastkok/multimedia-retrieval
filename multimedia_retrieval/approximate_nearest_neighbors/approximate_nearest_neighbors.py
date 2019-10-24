from annoy import AnnoyIndex
import random
import numpy as np


def approximate_nn(feature_db):

    n_rows, n_cols = feature_db.shape
    ann = AnnoyIndex(55, 'euclidean')

    for index, row in feature_db.iterrows():
        feature_vect = []
        for col_name in feature_db.columns:
            #  Its a histogram
            if isinstance(row[col_name], tuple):
                hist_vals = row[col_name][0]
                for val in hist_vals:
                    feature_vect.append(val)
            else:
                feature_vect.append(row[col_name])
        ann.add_item(index, feature_vect)

    ann.build(10)
    # Gets the 5 nearest items that are closest to 61.
    print(ann.get_nns_by_item(61, 5))