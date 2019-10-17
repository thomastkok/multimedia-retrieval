import numpy as np
import matplotlib.pyplot as plt
import math
import csv


#  Perhaps useful to look at bin sizes.
#  https://www.statisticshowto.datasciencecentral.com/choose-bin-sizes-statistics/


def plot_histogram(title, nr_bins, mn, mx, **kwargs):
    """
    Plots one or more histograms (as subplots) given a specified bin size.
    The histograms share the y-axis (the counts).
    """

    config = dict(alpha=0.5, bins=nr_bins)

    fig, axs = plt.subplots(1, len(kwargs), sharey=True, squeeze=False)

    i = 0
    for kw in kwargs.keys():
        axs[0, i].hist(kwargs[kw], alpha=0.5, facecolor='green', edgecolor='k',
                       range=(mn, mx), bins=nr_bins)
        axs[0, i].set_title(kw)
        i += 1
    plt.suptitle(title)
    plt.subplots_adjust(hspace=0.5)
    plt.show()
