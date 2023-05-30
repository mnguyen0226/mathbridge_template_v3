```python
## This exercise requires you to have Numpy installed
## Checkout - https://numpy.org/doc/stable/index.html

## This exercise requires you to have Numpy installed
## Checkout - https://numpy.org/doc/stable/index.html

import numpy as np
from matplotlib import pyplot as plt

print("Generating a Uniform Distribution")
print("Please enter your desired low,high and  Number of Samples")

## Gets the Input necessary to generate a Normal Distribution
lb=float(input("Enter your lower bound:"))
hb=float(input("Enter your upper bound:"))
n_samples=int(input("Enter your Desired Number of Samples:"))

## Normal Distribution generated using numpy
uniform_dist = np.random.uniform(lb,hb, n_samples)

plt.hist(uniform_dist)
plt.show()
```