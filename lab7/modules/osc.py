import numpy as np
import math
from scipy import signal

class WaveGen(object):
    
    def __init__(self, sample_rate = 44100):
        #default sample sate is 44100

        self._frequency = 0
        self._amplitude = 0
        self._phase = 0
        self._sample_rate = sample_rate
        

    
    def cal_phase(self):
        pass



