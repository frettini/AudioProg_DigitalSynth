import math
import abc
from abc import ABC, abstractmethod

class Gen(ABC):
    
    def __init__(self, sampleRate = 44100):
        #default sample sate is 44100

        self._frequency = 0
        self._amplitude = 0
        self._phase = 0
        self._sample_rate = sampleRate
        

    @abc.abstractmethod
    def gen_buffer(self, bufferSize):
        pass



