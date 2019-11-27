from modules import delay, rec_osc, white_noise, filter
import numpy as np
import matplotlib.pyplot as plot
import scipy.fftpack

osc = rec_osc.RecOsc(20, 0.5)
white = white_noise.WhiteNoise()

d = delay.Delay(10, 2)
g = delay.Gain(2)
f = filter.Filter(0.99, 0.1425, 1., 0.0)

# f.a1 = 0
# f.a2 = -1
# f.b1 = -1.7553711
# f.b2 = 0.9025

#use scipy.signal.iirfilter to get coefficients "sos" mode

buffer1 = np.zeros(2048)

# og1 = osc.gen_buffer(2048, end_freq = 15000)
white_buffer = white.gen_buffer(204800)
result = f.filtering(white_buffer)
# white_freq = scipy.fftpack.fft(og1)
result_freq = scipy.fftpack.fft(result)


plot.plot(np.real(result_freq))
plot.show()
