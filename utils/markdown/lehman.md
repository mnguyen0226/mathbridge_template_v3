We are using a basic lehman generator, for generating our random values in this examples.

Here, the generator generates a new random value at each call, once we define a bunch of parameters and set a seed.

The four parameters of interest in this example are
```
r_seed - a generative seed used to generate random values.
m - a prime number (preferably very large) which is used for modulo operation.
a,q,r - some random initialization of variables to aid in generation
```
Given an initial seed configuration, the Lehman Generator recursively generates pseudo Random numbers!

Using the Lehman Generator, we generate three distinct sequences.

$U_n=Lehman(n)$ 

$V_n=\frac{1}{n}(U_1+U_2+......U_n)$

$W_n=\sqrt{n}(V_n-\alpha)$

Let $\alpha = 0.5$, in this case