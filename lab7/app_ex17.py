from modules import delay, rec_osc, white_noise, filter, soundrw
import numpy as np
import matplotlib.pyplot as plot
import scipy.fftpack
import scipy.signal

cutoff_freq = 1500
sample_rate = 44100
wp = 1500/44100
ws = 10000/44100
gpass = 1
gstop = 40
coefs = scipy.signal.iirdesign(wp,ws,gpass,gstop,output='sos')

print(coefs)


#read write sound file method
rw = soundrw.SoundRW()

# inst recursive oscillator and white noise generator
osc = rec_osc.RecOsc(20, 0.5)
white = white_noise.WhiteNoise()

# inst a delay, gain and filter object
d = delay.Delay(10, 2)
g = delay.Gain(2)
f1 = filter.Filter(0.99999, 0.1, 0.9, 0.1)
f2 = filter.Filter(0.99999, 0.1, 0.9, 0.1)

f1.setcoef(coefs[0,0], coefs[0,1], coefs[0,2], coefs[0,3], coefs[0,4], coefs[0,5])
f2.setcoef(coefs[1,0], coefs[1,1], coefs[1,2], coefs[1,3], coefs[1,4], coefs[1,5])
# og1 = osc.gen_buffer(2048, end_freq = 15000)

# Generate and filter the buffer
white_buffer = white.gen_buffer(204800) # gen white buffer

result = f1.gen_buffer(white_buffer) # filter it 
#result = f2.gen_buffer(result) # filter it 
norm_result = result/np.max(result) # normalize result (avoid blown filters)
result_freq = scipy.fftpack.fft(result) # get spectrum

# Write noise to wav
rw.write_wav(white_buffer, 44100, "white_noise")
rw.write_wav(norm_result, 44100, "white_noise_filter")


plot.plot(np.real(result_freq))
# plot.plot(norm_result)
plot.show()


#use scipy.signal.iirfilter to get coefficients "sos" mode
