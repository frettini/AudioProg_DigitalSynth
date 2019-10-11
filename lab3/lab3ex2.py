import numpy as np
import scipy.io.wavfile
import math


def create_frequency(sample_rate, offset = 0):
    user_freq = 1
    time = np.arange(0, 44100)
    result = np.zeros(len(time))
    count = 0

    while user_freq != 0:

        print("provide frequency :")
        user_freq = input()
        user_freq = int(user_freq)
        result += np.sin(time/sample_rate * 2*math.pi * int(user_freq) + offset) 
        count += 1 
    
    return result/np.max(result)
    
def write_wav(samples, sample_rate, name):

    convert_16_bit = float(2**15)
    samples = np.int16( samples * convert_16_bit )
    print("Data type is now:", samples.dtype)

    scipy.io.wavfile.write("{}.wav".format(name), sample_rate, samples)

sample_rate = 44100
file_name = "test1"


samples = create_frequency(sample_rate)
write_wav(samples, sample_rate, file_name) 