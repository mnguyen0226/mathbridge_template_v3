```python
## This exercise requires you to have Numpy installed
## Checkout - https://numpy.org/doc/stable/index.html

import numpy as np
from matplotlib import pyplot as plt

print("Generating a Poisson Distriution")
print("Please enter your desired Lambda and  Number of Samples")

## Gets the Input necessary to generate a Normal Distribution
lambdaEvents=int(input("Enter your Desired Rate of events:"))
n_samples=int(input("Enter your Desired Number of Samples:"))

## Normal Distribution generated using numpy
poisson_dist = np.random.poisson(lambdaEvents, n_samples)

plt.hist(poisson_dist)
plt.show()
```