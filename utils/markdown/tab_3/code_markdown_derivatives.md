Derivatives of a function can be obtained by utilizing one of the three methods

- By differentiating the original equation
- By defining a small interval and arriving at the derivative by utilizing the formula
  - $\Delta(y) = \frac{f(y+d)-f(y)}{d}$
- Another interesting way to compute gradients programmatically is using autograd, which is the gradient evaluator of choice in most modern Neural Network packages like Pytorch. 
  - It is useful for computing gradients of complex functions of the form 
    - f(y)=g(t(l(s(x)))), where a function is a chain of functions
    - This is extremely powerful in matrix differentiation.
    - To read more on the design of autograd, please have a look at the documentation -https://pytorch.org/tutorials/beginner/blitz/autograd_tutorial.html

You will find an implementation to plot gradients and visualize the same in Python