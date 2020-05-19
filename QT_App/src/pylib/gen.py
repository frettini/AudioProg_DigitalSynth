import abc
from abc import ABC, abstractmethod
import math
import numpy as np
from scipy import signal

class Generator(ABC):
    """
    Abstract Base Class for an audio generator.

    Accepts an optional sample rate which is 44100 by default
    An audio buffer is generated using the genBuffer method.
    The frequency of the generator is generated using the setFreq method. 
    """

    def __init__(self, sample_rate = 44100):
        #default sample sate is 44100
        # think about removing the amplitude and phase
        self._frequency = 0
        self._sampleRate = sample_rate
        

    @abc.abstractmethod
    def genBuffer(self, bufferSize):
        """ Return an array of size bufferSize containing audio samples. """
        pass
    
    @abc.abstractmethod
    def setFreq(self, freq):
        """ Sets the frequency of the audio generator. """
        pass



