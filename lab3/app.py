import math

import scipy.io.wavfile
import numpy as np
import matplotlib.pyplot as plt
from modules import soundrw, sine_oscillator

SAMPLE_RATE = 44100
BUFFER_SIZE = 2048
filename = "test2"

#initialize waves into variables
sineosc = sine_oscillator.SineOsc(SAMPLE_RATE)

#initialize the sound interface to read and write 
sound = soundrw.SoundRW()

#store osc in dictionnary for user input
input_dict = {"sine" : sineosc}

combined_sample = np.array([])

#specify duration of sound in second and break it in number of buffer waves
duration = input("Specify duration of sound in seconds: ") 
buffer_counts = int(float(duration) * SAMPLE_RATE / BUFFER_SIZE)

#specify the type of signal wanted for the duration
user_signal = input("Specify Osc : sine/saw/square: ")
osc = input_dict.get(user_signal, "Invalid input")

#specify the frequency and amplitude of the signal
osc.frequency = int(input("provide frequency: "))
osc.amplitude = float(input("provide amplitude between 0 and 1: "))

buffer = np.zeros(BUFFER_SIZE)

print(buffer_counts)
#generate wave for each buffer
for i in range(buffer_counts):
    buffer = osc.gen_buffer(BUFFER_SIZE)
    combined_sample = np.append(combined_sample, buffer)


plt.plot(combined_sample)
plt.show()
    
sound.write_wav(combined_sample, 44100, filename)