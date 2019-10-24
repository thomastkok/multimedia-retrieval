import numpy as np


def hist_convert(hist_string):
    vals = hist_string[1:-1].replace('array', 'np.asarray').split(', np')
    vals[1] = 'np' + vals[1]
    return eval(vals[0]), eval(vals[1])