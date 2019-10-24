import numpy as np
import matplotlib.pyplot as plt
import math
import csv

from multimedia_retrieval.descriptors.helpers import get_hist_ranges

#  Perhaps useful to look at bin sizes.
#  https://www.statisticshowto.datasciencecentral.com/choose-bin-sizes-statistics/


def plot_histogram(title, nr_bins, n_rows_cols=None, **kwargs):
    """
    Plots one or more histograms (as subplots) given a specified bin size.
    And an optional tuple containing the number of rows/cols of the subplots.
    The histograms share the y-axis (the counts).
    """

    num_plots = len(kwargs)
    hist_ranges = get_hist_ranges()
    fig, axs = None, None

    if isinstance(n_rows_cols, tuple):
        n_rows, n_cols = n_rows_cols
        if num_plots > n_cols * n_rows:
            raise ValueError(
                "Too many histograms to plot. Give another dimension.")
        else:
            fig, axs = plt.subplots(
                nrows=n_rows, ncols=n_cols, sharey=True,  squeeze=False)
    else:
        fig, axs = plt.subplots(nrows=1, ncols=len(
            kwargs), sharey=True, squeeze=False)

    faxs = axs.reshape(-1)
    num_axs = len(faxs)

    i = 0

    for kw in kwargs.keys():
        mn_mx = hist_ranges[kw]
        faxs[i].hist(kwargs[kw], alpha=0.5, facecolor='green', edgecolor='k',
                     range=mn_mx, bins=nr_bins)
        faxs[i].set_title(kw)
        faxs[i].set_xlim(mn_mx)
        i += 1

    unused_axs = -(num_axs - num_plots)

    if unused_axs < 0:
        for i in list(range(num_axs))[unused_axs:]:
            fig.delaxes(faxs[i])

    plt.suptitle(title)
    plt.subplots_adjust(hspace=0.5)
    plt.show()
