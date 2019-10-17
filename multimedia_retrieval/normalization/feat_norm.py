from numpy import std, mean


def rescale(feature):
    """
    Rescales the feature values to [0, 1].

    Args:
        feature (pd.Series): All values of this feature in the dataset.

    """
    lo = min(feature)
    hi = max(feature)
    feature[:] = [(x - lo) / (hi - lo) for x in feature]


def standardize(feature):
    """
    Rescales the feature values to a mean of 0,
    with new feature values equal to standard deviation from original mean.

    Args:
        feature (pd.Series): All values of this feature in the dataset.

    """
    avg = mean(feature)
    sd = std(feature)
    feature[:] = [(x - avg) / sd for x in feature]


def normalize_histogram(feature):
    """
    Normalizes all histograms to a total area of 1.

    Args:
        feature (pd.Series): List of histograms.

    """
    for histogram in feature:
        bins = histogram[0]
        bs = bins.sum()
        bins = [x / bs for x in bins]


def rescale_to(value, min, max):
    """Rescales a single feature value to a certain range."""
    return (value - min) / (max - min)


def standardize_to(value, mean, sd):
    """Standardizes a certain feature value to a certain distribution."""
    return (value - mean) / sd
