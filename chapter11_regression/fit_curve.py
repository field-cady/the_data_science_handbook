from scipy.optimize import curve_fit
import numpy as np

xs = np.array([1.0, 2.0, 3.0, 4.0])
ys = 2.0 + 3.0 *xs*xs + 0.2*np.random.uniform(3)
def calc(x, a, b):
    return a + b*x*x

cf = curve_fit(calc, xs, ys)
best_fit_params = cf[0]
