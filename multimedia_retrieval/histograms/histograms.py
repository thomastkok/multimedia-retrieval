import numpy as np
import matplotlib.pyplot as plt
import math
import csv

#  Perhaps useful to look at bin sizes.
#  https://www.statisticshowto.datasciencecentral.com/choose-bin-sizes-statistics/


def get_histogram(arr, nr_bins):
    return np.histogram(arr, nr_bins)


def get_uniform_bins(min, max, nr_bins):
    bin_range = int(math.ceil(max)-math.floor(min))
    hist_bins = []
    bin_stepsize = int(math.ceil(bin_range / nr_bins))
    for i in range(0, bin_range, bin_stepsize):
        hist_bins.append(i)
    return hist_bins


def plot_histogram(arr, min, max, nr_bins):
    hist_bins = get_uniform_bins(min, max, nr_bins)
    n, bins, patches = plt.hist(arr, hist_bins, facecolor='green', alpha=0.5)
    plt.show()
