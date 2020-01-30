from modules import delay, rec_osc, white_noise, filter, soundrw
import numpy as np
import matplotlib.pyplot as plot
import scipy.fftpack
import scipy.signal
import os
import time

#read write sound file method
rw = soundrw.SoundRW()

# inst recursive oscillator and white noise generator
osc = rec_osc.RecOsc(20, 0.5)
white = white_noise.WhiteNoise()

sample_rate = 44100

# initialize frequency coeffs
wp = 1600*2/sample_rate # multiply by two for nyquist frequency
ws = 1400*2/sample_rate
gpass = 1
gstop = 40
coefs = scipy.signal.iirdesign(wp,ws,gpass,gstop,output='sos')

print(coefs)

#instantiate filters with calculated coefficients 
filters = []
for i in range(coefs.shape[0]):
    temp_fil = filter.Filter(0.99999, 0.1, 0.9, 0.1) #inst
    temp_fil.setcoef(coefs[i,0], coefs[i,1], coefs[i,2], coefs[i,3], coefs[i,4], coefs[i,5])
    filters.append(temp_fil)


# inst a delay, gain and filter object
d = delay.Delay(10, 2)
g = delay.Gain(2)

# og1 = osc.gen_buffer(2048, end_freq = 15000)

# Generate and filter the buffer
cwd = os.getcwd()
filename = os.path.join(cwd,"voice1.wav")
print(filename)
white_buffer = rw.load_wav(filename) #white.gen_buffer(204800) # gen white buffer
to_filter = white_buffer

#loop through instantiated filters
for fil in filters:
    to_filter = fil.gen_buffer(to_filter) 

norm_result = to_filter/np.max(to_filter) # normalize result (avoid blown filters)
result_freq = scipy.fftpack.fft(norm_result) # get spectrum

# Write noise to wav
# rw.write_wav(white_buffer, 44100, "white_noise")
rw.write_wav(norm_result, 44100, "voice1_filter")


plot.plot(np.real(result_freq))
# plot.plot(norm_result)
plot.show()


