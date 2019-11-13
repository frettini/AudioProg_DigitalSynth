from modules import delay, rec_osc, white_noise, filter
import numpy as np
import matplotlib.pyplot as plot
import scipy.fftpack

osc = rec_osc.RecOsc(206, 0.5)
white = white_noise.WhiteNoise()

d = delay.Delay(10, 2)
g = delay.Gain(2)
f = filter.Filter(0.99, 0.62659, 0.9, 0.62659)

buffer1 = np.zeros(2048)
buffer2 = np.zeros(2048)

og1 = osc.gen_buffer(2048)
og2 = osc.gen_buffer(2048)

og = np.concatenate((og1, og2))

white_buffer = white.gen_buffer(2048)

result = f.filtering(white_buffer)

white_freq = scipy.fftpack.fft(white_buffer)
result_freq = scipy.fftpack.fft(result)

plot.plot(og)
# plot.plot(white_freq)
plot.show()
