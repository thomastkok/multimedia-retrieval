import numpy as np
import matplotlib.pyplot as plt
import math
import csv


#  Perhaps useful to look at bin sizes.
#  https://www.statisticshowto.datasciencecentral.com/choose-bin-sizes-statistics/


def plot_histogram(arr, nr_bins):
    """
    Plots a histogram given a specified bin size.
    """
    n, bins, patches = plt.hist(
        arr, nr_bins, edgecolor='k', facecolor='green', alpha=0.5)
    plt.show()
