from .gen import Gen
import numpy as np
import math

class WhiteNoise(Gen):

    def __init__(self, sample_rate = 44100):
        super().__init__(sample_rate)
        self.mean = 0
        self.std = 0

    def gen_buffer(self, buffer_size):
        result = np.zeros(buffer_size)
        result =  np.random.standard_normal(size=buffer_size)
        return result/np.max(result)