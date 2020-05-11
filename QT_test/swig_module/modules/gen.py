import numpy as np
import math
import abc
from abc import ABC, abstractmethod
from scipy import signal

class Generator(ABC):
    
    def __init__(self, sample_rate = 44100):
        #default sample sate is 44100

        self._frequency = 0
        self._amplitude = 0
        self._phase = 0
        self._sampleRate = sample_rate
        

    @abc.abstractmethod
    def genBuffer(self, bufferSize):
        pass
    
    @abc.abstractmethod
    def setFreq(self, freq):
        pass



