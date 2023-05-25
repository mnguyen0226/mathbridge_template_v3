import numpy as np


def generatedydx(a, func):
    a_list = list(a)
    dydx_list = []
    n = len(a)
    i = 0
    d = a[1] - a[0]
    while i < n:
        fx = func(a[i])
        fx_1 = func(a[i] + d)
        g = (fx_1 - fx) / d
        dydx_list.append(g)
        i += 1
    return np.asarray(dydx_list)
