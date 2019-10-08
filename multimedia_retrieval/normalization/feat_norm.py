from numpy import std, mean


def rescale(feature):
    lo = min(feature)
    hi = max(feature)
    feature[:] = [(x - lo) / (hi - lo) for x in feature]


def standardize(feature):
    avg = mean(feature)
    sd = std(feature)
    feature[:] = [(x - avg) / sd for x in feature]


def normalize_histogram(feature):
    for histogram in feature:
        all_bins = sum(histogram)
        histogram[:] = [x / all_bins for x in feature]
