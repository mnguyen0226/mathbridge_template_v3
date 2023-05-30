```python
import matplotlib.pyplot as plt
import numpy as np
import random
import sys

def generateUniformDistributionfromNumpy(n):
    gen=np.random.uniform(0, 1, 10)
    return gen

## This class generates random numbers using lehman generator
## Allows for a seed to be set and reset, and can return one/n uniform random values as required
## Also generated U_n, V_n and W_n series as discussed in the playground
class RandTool:
    def __init__(self,m=2147483647,a=48271,q=44488,r=3399,r_seed=12345678):
        self.m=m
        self.a=a
        self.q=q
        self.r=r
        self.r_seed=r_seed

    def setSeed(seed):
        random.seed(seed)

    def getRandom(self):
        self.rand = random.randint(-sys.maxsize - 1, sys.maxsize)
        return self.rand

    ## uniform - [0,1]
    def getUniformValue(self):
        hi = int(self.r_seed / self.q)
        lo = int(self.r_seed - self.q * hi)
        t = (self.a * lo) - (self.r * hi)
        if t > 0:
            self.r_seed = t
        else:
           self.r_seed = t + self.m
        uniform= float(self.r_seed)/float(self.m)
        return uniform

    def getUniformDist(self,n):
        uniform=[]
        for i in range(n):
            uniform.append(self.getUniformValue())
        return uniform

    def getUniformV(self,dist):
        sum=0.0
        vlist=[]
        for i in range(len(dist)):
            sum+=dist[i]
            vlist.append(sum/(i+1))
        return vlist

    def getUniformW(self,dist,scaledown=0.5):
        wlist=[]
        for i in range(len(dist)):
            wlist.append(np.sqrt(i+1)*(dist[i]-scaledown))
        return wlist


    def getUniformUVW(self,n,scaledown=0.5):
        u=self.getUniformDist(n)
        v=self.getUniformV(u)
        w=self.getUniformW(v,scaledown)
        return u,v,w

rand=RandTool()

def main():
    ### To get the uniform distribution U_n,V_n,W_n
    ## Takes in n and alpha
    print("Please enter the number of samples:")
    n=int(input())
    print("Please enter the number of Bins:")
    bins=int(input())
    print("Please enter an appropriate alpha for the W distribution")
    alpha=float(input())
    U,V,W=rand.getUniformUVW(n,alpha)
    ## Change the bins as desired
    plt.hist(U,bins=10)
    plt.show()
    plt.hist(V,bins=10)
    plt.show()

    plt.hist(W,bins=10)
    plt.show()


if __name__ == "__main__":
    main()
```