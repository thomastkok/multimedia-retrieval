import numpy as np
import matplotlib.pyplot as plt
import csv

#  Perhaps useful to look at bin sizes.
#  https://www.statisticshowto.datasciencecentral.com/choose-bin-sizes-statistics/


def plot_histogram(arr, min, max, nr_bins):    
    bin_range = int(max - min)
    hist_bins = []
    bin_stepsize = int(bin_range / nr_bins)
    for i in range(0, bin_range, bin_stepsize):
        hist_bins.append(i)

    n, bins, patches = plt.hist(arr, hist_bins, facecolor='green', alpha=0.5)
    print(bins)
    plt.show()

def import_csv(file_path):
    with open(file_path, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            print(row)
