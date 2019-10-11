import math

import scipy.io.wavfile
import numpy as np
from modules import soundrw, oscillator
import matplotlib.pyplot as plt


SAMPLE_RATE = 44100
BUFFER_SIZE = 2048
filename = "test2"
sample_count = 0

#initialize waves into variables
sineosc = oscillator.SineOscillator(BUFFER_SIZE, SAMPLE_RATE)
sawosc = oscillator.SawOscillator(BUFFER_SIZE, SAMPLE_RATE)
squareosc = oscillator.SquareOscillator(BUFFER_SIZE, SAMPLE_RATE)

#store osc in dictionnary for user input
input_dict = {"sine" : sineosc, "saw": sawosc, "square": squareosc}

#initialize the sound interface to read and write 
sound = soundrw.SoundRW()

#create empty array
combined_sample = np.zeros(0)


#specify duration of sound in second and break it in number of buffer waves
duration = input("Specify duration of sound in seconds: ") 
buffer_counts = int(float(duration) * SAMPLE_RATE / BUFFER_SIZE)
sample_results = np.zeros((buffer_counts, BUFFER_SIZE))


while True:
    #specify the type of signal wanted for the duration
    user_signal = input("Specify Osc : sine/saw/square: ")
    osc = input_dict.get(user_signal, "Invalid input")


    #specify the frequency and amplitude of the signal
    osc.frequency = int(input("provide frequency: "))
    osc.amplitude = float(input("provide amplitude between 0 and 1: "))
    
    #generate wave for each buffer
    for i in range(buffer_counts):
        sample_count = i * BUFFER_SIZE
        sample_results[i,:]  = osc.gen_wave(sample_count, sample_results[i,:])

    #check if the user wants to add signal components to the waves
    c = input("Do you want to add a signal component? [Y/N] ")

    if  c == "N":
        break
    else :
        continue


#combine all the buffers together
for i in range(buffer_counts):

    combined_sample = np.append(combined_sample, sample_results[i])

#result_sample = np.append(result_sample, samples)

plt.plot(combined_sample)
plt.show()
    
sound.write_wav(combined_sample, 44100, filename)

