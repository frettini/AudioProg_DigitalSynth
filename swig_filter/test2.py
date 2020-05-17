from modules import rec_osc, white_noise, soundrw
import numpy as np
import matplotlib.pyplot as plot
import scipy.fftpack
import scipy.signal
import time 

from pkg import swig_filter as sf

sample_rate = 44100
wp = [400*2/sample_rate, 401*2/sample_rate ]    # multiply by two for nyquist frequency
ws = [350*2/sample_rate, 450*2/sample_rate ]
gpass = 10
gstop = 100
coefs = scipy.signal.iirdesign(wp,ws,gpass,gstop,output='sos', ftype='ellip')

print(type(scipy.signal.iirpeak(400*2/sample_rate, 5))) 

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
filt_bank = sf.FilterChain(coefs)
filt_bank.setCoef(coefs)
print("test2")
# og1 = osc.gen_buffer(2048, end_freq = 15000)

# Generate and filter the buffer
white_buffer = white.gen_buffer(204800) # gen white buffer
result = np.zeros(len(white_buffer))

start = time.time()
filt_bank.genBuffer(result, np.array(white_buffer)) # filter it 
end = time.time()
print("time elapsed: {}".format(end-start))

norm_result = result/np.max(abs(result)) # normalize result (avoid blown filters)
result_freq = scipy.fftpack.fft(norm_result) # get spectrum



# Write noise to wav
rw.write_wav(white_buffer, 44100, "white_noise")
rw.write_wav(norm_result, 44100, "white_noise_filter")

print("test4")


#use scipy.signal.iirfilter to get coefficients "sos" mode
# plot.plot(result)
# plot.plot(norm_result)

# plot.plot(white_buffer)
plot.plot(np.real(result_freq))
plot.show()

filt_bank = None