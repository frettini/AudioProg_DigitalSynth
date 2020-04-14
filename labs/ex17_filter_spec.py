from modules import delay, rec_osc, white_noise, filter, soundrw
import numpy as np
import matplotlib.pyplot as plot
import scipy.fftpack
import scipy.signal
import os
import time

#read write sound file method
rw = soundrw.SoundRW()

# inst white noise generator
white = white_noise.WhiteNoise()
sample_rate = 44100

sample_rate = 44100
wp = [400*2/sample_rate, 401*2/sample_rate ]    # multiply by two for nyquist frequency
ws = [350*2/sample_rate, 450*2/sample_rate ]
gpass = 10
gstop = 120
coefs = scipy.signal.iirdesign(wp,ws,gpass,gstop,output='sos', ftype='ellip')

print(coefs)

#instantiate filters with calculated coefficients 
filters = []
for i in range(coefs.shape[0]):
    temp_fil = filter.Filter(0.99999, 0.1, 0.9, 0.1) #inst
    temp_fil.setcoef(coefs[i,:])
    filters.append(temp_fil)


# inst a delay, gain and filter object
d = delay.Delay(10, 2)
g = delay.Gain(2)

# og1 = osc.gen_buffer(2048, end_freq = 15000)

# Generate and filter the buffer
cwd = os.getcwd()
# filename = os.path.join(cwd,"assets", "voice1.wav")
# print(filename)
white_buffer =  white.gen_buffer(204800) # gen white buffer #rw.load_wav(filename)
to_filter = white_buffer

start = time.time()
#loop through instantiated filters
for fil in filters:
    to_filter = fil.gen_buffer(to_filter) 
end = time.time()
print("time elapsed: {}".format(end-start))

norm_result = to_filter/np.max(to_filter) # normalize result
result_freq = scipy.fftpack.fft(norm_result) # get spectrum

# Write noise to wav
# rw.write_wav(white_buffer, 44100, "white_noise")
# rw.write_wav(norm_result, 44100, "assets/voice1_filter")


plot.plot(np.real(result_freq))
# plot.plot(norm_result)
plot.show()


