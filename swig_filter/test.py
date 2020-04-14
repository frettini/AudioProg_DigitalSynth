from modules import rec_osc, white_noise, soundrw
import numpy as np
import matplotlib.pyplot as plot
import scipy.fftpack
import scipy.signal

import swig_filter as sf

sample_rate = 44100
wp = 400*2/sample_rate # multiply by two for nyquist frequency
ws = 500*2/sample_rate
gpass = 40
gstop = 160
coefs = scipy.signal.iirdesign(wp,ws,gpass,gstop,output='sos')

# wp2 = 2000*2/sample_rate # multiply by two for nyquist frequency
# ws2 = 200*2/sample_rate
# gpass2 = 1
# gstop2 = 40
# coefs2 = scipy.signal.iirdesign(wp2,ws2,gpass2,gstop2,output='sos')

# coefs = np.concatenate((coefs,coefs2))
print(coefs)


print("test1")
#read write sound file method
rw = soundrw.SoundRW()

# inst recursive oscillator and white noise generator
# osc = rec_osc.RecOsc(20, 0.5)
white = white_noise.WhiteNoise()

# inst a delay, gain and filter object
# pole magnitude distance to 1 = Q 
# difference between zero and poles = gain
print(coefs[0,:])
filt_bank = []
filt_num = coefs.shape[0] 
for i in range(filt_num):
    filt_bank.append(sf.Filter(coefs[i,:])) #pole mag, pole ang, zero mag, zero ang

print("test2")
# og1 = osc.gen_buffer(2048, end_freq = 15000)

# Generate and filter the buffer
white_buffer = white.gen_buffer(204800) # gen white buffer
result = np.zeros(len(white_buffer))

for i in range(filt_num):
    filt_bank[i].genBuffer(result, np.array(white_buffer)) # filter it 


norm_result = result/np.max(result) # normalize result (avoid blown filters)
result_freq = scipy.fftpack.fft(norm_result) # get spectrum


# Write noise to wav
rw.write_wav(white_buffer, 44100, "white_noise")
rw.write_wav(norm_result, 44100, "white_noise_filter")

print("test4")
#use scipy.signal.iirfilter to get coefficients "sos" mode
# plot.plot(norm_result)
# plot.plot(white_buffer)
plot.plot(np.real(result_freq))
plot.show()

filt_bank = None