#from sympy import N, false
import numpy as np
import os

w = 5
h_total = 16

t_left = (h_total,w,3)
h_steps = h_total // w

A = np.arange(h_total)


for i in range(0,h_total,w):
    print(A[i:i+w])




# Slump = np.random.randint(0,10,t_left)



# print(Slump)
# print(Slump[:2])
