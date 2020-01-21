from modules import delay, rec_osc, white_noise, filter, soundrw
import numpy as np
import matplotlib.pyplot as plot
import scipy.fftpack
import scipy.signal

coefs = scipy.signal.iirfilter(1,[0.05, 0.1])



#read write sound file method
rw = soundrw.SoundRW()

# inst recursive oscillator and white noise generator
osc = rec_osc.RecOsc(20, 0.5)
white = white_noise.WhiteNoise()

# inst a delay, gain and filter object
d = delay.Delay(10, 2)
g = delay.Gain(2)
f = filter.Filter(0.99999, 0.1, 0.9, 0.1)

# f.a0 = 1
# f.a1 = 0
# f.a2 = -1
# f.b0 = 1
# f.b1 = -1.7553711
# f.b2 = 0.9025

# og1 = osc.gen_buffer(2048, end_freq = 15000)

# Generate and filter the buffer
white_buffer = white.gen_buffer(204800) # gen white buffer
result = f.gen_buffer(white_buffer) # filter it 
norm_result = result/np.max(result) # normalize result (avoid blown filters)
result_freq = scipy.fftpack.fft(result) # get spectrum

# Write noise to wav
rw.write_wav(white_buffer, 44100, "white_noise")
rw.write_wav(norm_result, 44100, "white_noise_filter")


plot.plot(np.real(result_freq))
# plot.plot(norm_result)
plot.show()


#use scipy.signal.iirfilter to get coefficients "sos" mode
