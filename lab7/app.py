from modules import delay, rec_osc, white_noise
import numpy as np
import matplotlib.pyplot as plot

osc = rec_osc.RecOsc(440, 0.5)
white = white_noise.WhiteNoise()

"""
d = delay.Delay(500)
g = delay.Gain(2)

buffer1 = np.zeros(2048)
buffer2 = np.zeros(2048)

og1 = osc.gen_buffer(2048)
buffer1 = d.delay(og1)
buffer1 = g.scale(buffer1)

og2 = osc.gen_buffer(2048)
buffer2 = d.delay(og2)
buffer2 = g.scale(buffer2)

original_buffer = np.concatenate((og1, og2))
buffer = np.concatenate((buffer1,buffer2))

white_buffer = white.gen_buffer(2048)
"""

d = delay.Delay(10, 2)
print(d.process(2.0))
print(d.process(3.5))
print(d.process(-1.0))

#plot.plot(white_buffer)

#plot.show()
