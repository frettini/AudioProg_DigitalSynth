import numpy as np
import matplotlib.pyplot as plot


import math

def sinwave(time, frequency, offset = 0):
    return np.sin(time*2*math.pi*frequency + offset)




time = np.arange(0, 0.01, 0.0001)
#amplitude = np.sin(time*2*math.pi*100)

sin100 = sinwave(time, 100)
sin440 = sinwave(time, 440)
sin440of = sinwave(time, 440,math.pi/2)
plot.plot(time, sin100)
plot.plot(time, sin440)
plot.plot(time, sin440of)

plot.show()
