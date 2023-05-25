import numpy as np
import autograd.numpy as agnp
from autograd import elementwise_grad

import matplotlib.pyplot as plt

# Computing Gradient with a defined distance
x = np.linspace(0, 10, 10000)  # Define a set of values as linearly spaced elements
dx = x[1] - x[0]  # Define dx, as the distance between the first two element of the set
fx = x**2 + 1  # Define the values of f(x) given x
dydx = np.gradient(
    fx, dx
)  # Use the values of f(x) and dx to compute gradients using the afforementioned formula


plt.plot(x, fx, label="$x^2+1$")
plt.plot(x, dydx, label="Approximate difference based Gradient")
plt.title("Plotting using a small difference")
plt.legend()
plt.show()

# Computing Gradient with a formula

x = np.linspace(0, 10, 10000)
fx = x**2 + 1
dydx = 2 * x

plt.plot(x, fx, label="$x^2+1$")
plt.plot(x, dydx, label="Formula Gradient")
plt.title("Plotting gradients after manually differentiating the function equation")
plt.legend()
plt.show()


# Computing elementwise gradient in Numpy
# Autograd allows for some interesting usecases, as functions with conditionals can be
# defined allowing for one to perform nice differentiations
def fx(x):
    return x**2 + 1


x = agnp.linspace(0, 10, 10000)
y = fx(x)
dydx = elementwise_grad(fx)(x)

plt.plot(x, y, label="$x^2+1$")
plt.plot(x, dydx, label="Elementwise Gradient")
plt.title("Plotting gradients using elementwise gradient")
plt.legend()
plt.show()
