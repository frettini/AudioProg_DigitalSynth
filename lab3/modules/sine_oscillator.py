import osc
import numpy as np
import math

class SineOsc(osc.WaveGen):

    def __init__(self, sample_rate = 44100):
        super().__init__(sample_rate)
        self.states = np.zeros(2)


    #properties setters and getters---------------------------------
    @property
    def frequency(self):
        print("get freq")
        return self.__frequency

    @frequency.setter
    def frequency(self, value):
        print("set freq")
        if value >= 0 or value <= self.__sample_rate/2:
            self.__frequency = value
        elif value > self.__sample_rate/2:
            self.__frequency = self.__sample_rate/2
        else:
            self.__frequency = 0

    @property
    def amplitude(self):
        print("get amp")
        return self.__amplitude

    @amplitude.setter
    def amplitude(self, value):
        print("set amp")
        if value >= 0 or value <= 1:
            self.__amplitude = value
        elif value > 1:
            self.__amplitude = 1
        else:
            self.__amplitude = 0
    
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
            print("going up boi")
            self.__phase = phase
        elif self.states[1] < self.states[0] :
            #going down
            print("going down bois")
            self.__phase = np.pi - phase


    def gen_buffer(self, buffer):
        #takes in a buffer of any size in the form of nparray

        self.buffer = np.arange(0,len(buffer))
        self.__phase = self.__phase % (2*math.pi)

        x = ((self.buffer * 2*math.pi * self.__frequency)/self.sample_rate) % (2*math.pi)
        result = self.__amplitude * np.sin(x + self.__phase)
        
        result = result/np.max(result)

        self.states = result[-2:]
        self.cal_phase()

        return result

