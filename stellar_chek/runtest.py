import roundcheck as rk
import numpy as np
#import pickle

vtest = np.vectorize(lambda t: rk.go_test(rk.cat, rk.data, t))

thresholds = range(2, 300, 1)

results = vtest(thresholds)

np.save('results_0.3.npy', results)