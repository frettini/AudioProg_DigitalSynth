from modules import rec_osc, white_noise, soundrw
import numpy as np
import matplotlib.pyplot as plot
import scipy.fftpack
import scipy.signal

import swig_filter

sample_rate = 44100
wp = 1600*2/sample_rate # multiply by two for nyquist frequency
ws = 1400*2/sample_rate
gpass = 1
gstop = 40
coefs = scipy.signal.iirdesign(wp,ws,gpass,gstop,output='sos')


print("test1")
#read write sound file method
rw = soundrw.SoundRW()

# inst recursive oscillator and white noise generator
# osc = rec_osc.RecOsc(20, 0.5)
white = white_noise.WhiteNoise()

# inst a delay, gain and filter object
# pole magnitude distance to 1 = Q 
# difference between zero and poles = gain
f = swig_filter.Filter(coefs[0]) #pole mag, pole ang, zero mag, zero ang

print("test2")
# og1 = osc.gen_buffer(2048, end_freq = 15000)

# Generate and filter the buffer
white_buffer = white.gen_buffer(204800) # gen white buffer
result = np.zeros(len(white_buffer))
print(type(white_buffer))

f.genBuffer(result, np.array(white_buffer)) # filter it 

norm_result = result/np.max(result) # normalize result (avoid blown filters)
result_freq = scipy.fftpack.fft(norm_result) # get spectrum
print(result)
# Write noise to wav
rw.write_wav(white_buffer, 44100, "white_noise")
rw.write_wav(norm_result, 44100, "white_noise_filter")


plot.plot(np.real(result_freq))
# plot.plot(norm_result)
plot.show()

print("test4")
#use scipy.signal.iirfilter to get coefficients "sos" mode
