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


    def set_gen(self, freq, amp):
        self.frequency = freq
        self.amplitude = amp
    
    def cal_phase(self):
        pass



class SineOscillator(Generator):

    name = "Sine"

    def __init__(self, sample_rate = 44100):
        #default sample sate is 44100

        self.__frequency = 0
        self.__phase = 0
        self.__amplitude = 0
        self.sample_rate = sample_rate

    def cal_phase(self):
        pass


    def gen_buffer(self, buffer):
        return "hello world"