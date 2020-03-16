from modules import rec_osc, white_noise, soundrw
import numpy as np
import matplotlib.pyplot as plot
import scipy.fftpack
import scipy.signal

import swig_filter as sf

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

print(coefs[2])
# inst a delay, gain and filter object
# pole magnitude distance to 1 = Q 
# difference between zero and poles = gain

filt_bank = []
filt_num = coefs.shape[0] 
for i in range(filt_num):
    filt_bank.append(sf.Filter(coefs[i,:])) #pole mag, pole ang, zero mag, zero ang

print("test2")
# og1 = osc.gen_buffer(2048, end_freq = 15000)

# Generate and filter the buffer
white_buffer = white.gen_buffer(204800) # gen white buffer
result = np.zeros(len(white_buffer))
print(type(white_buffer))

for i in range(filt_num):
    filt_bank[i].genBuffer(result, np.array(white_buffer)) # filter it 


norm_result = result/np.max(result) # normalize result (avoid blown filters)
result_freq = scipy.fftpack.fft(norm_result) # get spectrum
print(result[:50])
print(result[-50:])
yeet = result


# Write noise to wav
rw.write_wav(white_buffer, 44100, "white_noise")
rw.write_wav(result, 44100, "white_noise_filter")

filt_bank = None


print("test4")
#use scipy.signal.iirfilter to get coefficients "sos" mode
plot.plot(yeet)
# plot.plot(norm_result)
plot.show()