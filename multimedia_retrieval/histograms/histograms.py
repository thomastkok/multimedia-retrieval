import numpy as np
import matplotlib.pyplot as plt
import math
import csv


#  Perhaps useful to look at bin sizes.
#  https://www.statisticshowto.datasciencecentral.com/choose-bin-sizes-statistics/


def get_histogram(arr, nr_bins):
    return np.histogram(arr, nr_bins)


def plot_histogram(arr, nr_bins):
    n, bins, patches = plt.hist(arr, nr_bins, edgecolor='k', facecolor='green', alpha=0.5)
    plt.show()
