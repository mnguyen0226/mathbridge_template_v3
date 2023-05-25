## This exercise requires you to have Numpy installed
## Checkout - https://numpy.org/doc/stable/index.html

import numpy as np
from matplotlib import pyplot as plt

print("Please enter your desired Mean, Standard Deviation and Number of Samples")

## Gets the Input necessary to generate a Normal Distribution
mean_norm = float(input("Enter your Desired Mean:"))
sd_norm = float(input("Enter your Desired Standard Deviation:"))
n_samples = int(input("Enter your Desired Number of Samples:"))

## Normal Distribution generated using numpy
norm_dist = np.random.normal(mean_norm, sd_norm, n_samples)

plt.hist(norm_dist)
plt.show()
