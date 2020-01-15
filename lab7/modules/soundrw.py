import numpy as np
import scipy.io.wavfile
import math


class SoundRW:

    def __init__(self):
        self.convert_16_bit = float(2**15)


    def write_wav(self, samples,sample_rate, name):

        convert_16_bit = float(2**15)
        samples = np.int16( samples * (self.convert_16_bit-1) )
        print("Data type is now:", samples.dtype)

        scipy.io.wavfile.write("{}.wav".format(name), sample_rate, samples)

    def load_wav(self, filename):
        sample_rate, samples = scipy.io.wavfile.read("{}".format)
        # scale to -1.0 -- 1.0
        samples = samples / convert_16_bit
        print("Data type is now:", samples.dtype)

        return samples



