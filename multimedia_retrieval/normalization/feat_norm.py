from numpy import std, mean


def rescale(feature):
    """
    Rescales the feature values to [0, 1].

    Args:
        feature (list[num]): All values of this feature in the dataset.

    """
    lo = min(feature)
    hi = max(feature)
    feature[:] = [(x - lo) / (hi - lo) for x in feature]


def standardize(feature):
    """
    Rescales the feature values to a mean of 0,
    with new feature values equal to standard deviation from original mean.

    Args:
        feature (list[num]): All values of this feature in the dataset.

    """
    avg = mean(feature)
    sd = std(feature)
    feature[:] = [(x - avg) / sd for x in feature]


def normalize_histogram(feature):
    """
    Normalizes all histograms to a total area of 1.

    Args:
        feature (list[list[num]]): List of histograms.

    """
    for histogram in feature:
        all_bins = sum(histogram)
        histogram[:] = [x / all_bins for x in feature]
