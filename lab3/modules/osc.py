import numpy as np
import math
from scipy import signal


class Generator(object):
    def gen_buffer(self, buffer):
        pass

class WaveGen(object):
    
    def __init__(self, sample_rate = 44100):
        #default sample sate is 44100

        self.__frequency = 0
        self.__amplitude = 0
        self.__phase = 0
        self.__sample_rate = sample_rate

    
    def cal_phase(self):
        pass



