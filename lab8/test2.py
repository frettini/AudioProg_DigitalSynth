import swig_filter as sf
import numpy as np

print("init")
a = np.double([[0,0,0,0,0,0],[1,1,1,1,1,1]])
f = sf.FilterChain(a)

print("clear")
f = None