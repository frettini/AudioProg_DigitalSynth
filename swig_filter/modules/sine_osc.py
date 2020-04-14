from .gen import Gen
import numpy as np
import math

class SineOsc(Gen):

    def __init__(self,  freq, amp, sample_rate = 44100):
        
        self.states = np.zeros(2)
        super().__init__(sample_rate)
        self._frequency = freq
        self._amplitude = amp 

    #properties setters and getters---------------------------------
    @property
    def frequency(self):
        print("get freq")
        return self._frequency

    @frequency.setter
    def frequency(self, value):
        print("set freq")
        if value >= 0 or value <= self._sample_rate/2:
            self._frequency = value
        elif value > self._sample_rate/2:
            self._frequency = self._sample_rate/2
        else:
            self._frequency = 0

    @property
    def amplitude(self):
        print("get amp")
        return self._amplitude

    @amplitude.setter
    def amplitude(self, value):
        print("set amp")
        if value >= 0 or value <= 1:
            self._amplitude = value
        elif value > 1:
            self._amplitude = 1
        else:
            self._amplitude = 0
    
    #-------------------------------------------------------------


    #sets the frequency and amplitude of the generator
    def set_gen(self, freq, amp):
        self.frequency = freq
        self.amplitude = amp



    #Calculate and return the phase of the 
    def cal_phase(self):
        phase = np.arcsin(self.states[1])

        if self.states[1] > self.states[0]:
            #going up
            self._phase = phase
        elif self.states[1] < self.states[0] :
            #going down
            self._phase = np.pi - phase


    def gen_buffer(self, buffer_size):
        #takes in a buffer of any size in the form of nparray
        self.buffer = np.arange(0,buffer_size)
        self._phase = self._phase % (2*math.pi)

        x = ((self.buffer * 2*math.pi * self._frequency)/self._sample_rate) % (2*math.pi)
        result = self._amplitude * np.sin(x + self._phase)
        result = result/np.max(result)

        self.states = result[-2:]
        self.cal_phase()

        return result

