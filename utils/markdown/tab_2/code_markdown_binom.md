```python
## This exercise requires you to have Numpy installed
## Checkout - https://numpy.org/doc/stable/index.html

import numpy as np
from matplotlib import pyplot as plt

print("Generating a Binomial Distribution")
print("Please enter your desired n,p and  Number of Samples")

## Gets the Input necessary to generate a Normal Distribution
n=int(input("Enter your Number of outcomes per event:"))
p=float(input("Enter your probability of success per event:"))
n_samples=int(input("Enter your Desired Number of Samples:"))

## Normal Distribution generated using numpy
binom_dist = np.random.binomial(n,p, n_samples)

plt.hist(binom_dist)
plt.show()
```