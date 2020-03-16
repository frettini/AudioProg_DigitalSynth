import swig_filter as sf
import numpy as np

print("init")
a = np.double([0,0,0,0,0,0])
f = sf.Filter(a)
f.setCoef(a)
input = np.zeros(10)
result = np.zeros(10)

print("gen buffer")
f.genBuffer(result, input)

print("clear")
f = None