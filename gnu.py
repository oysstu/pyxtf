from sympy import N, false
import numpy as np
import os


dir = "test"
if not os.path.isdir(dir):
    os.mkdir(dir)

for name in os.listdir():
    if name.endswith(".xtf"):
        print(name)