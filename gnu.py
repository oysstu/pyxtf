from sympy import N, false
import numpy as np
import os


dir = "test"
if not os.path.isdir(dir):
    os.mkdir(dir)

for file in os.listdir():
    if file.endswith(".xtf"):
        print(file)

colour = [1, 1, 31]/2

print(colour[2])