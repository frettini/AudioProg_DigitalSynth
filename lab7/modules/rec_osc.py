from .osc import WaveGen
import numpy as np
import math

class RecOsc(WaveGen):


    def __init__(self,  freq, amp, sample_rate = 44100):
        
        self.states = np.zeros(2)
        super().__init__(sample_rate)
        self._frequency = freq
        self._amplitude = amp 

        self.states[1] = math.sin(-1*2*math.pi*freq/sample_rate)
        self.states[0] = math.sin(-2*2*math.pi*freq/sample_rate)
        self.cos_omega_t = 2*math.cos(2*math.pi * freq /sample_rate)

        self.firstLoop = True


    #properties setters and getters---------------------------------
    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, value):
        if value >= 0 or value <= self._sample_rate/2:
            self._frequency = value
            self.change_freq()
            
        elif value > self._sample_rate/2:
            self._frequency = self._sample_rate/2
            self.change_freq()
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

    def change_freq(self):
        #need to recalculate the two previous samples with the new freq and phase
        self.states[0] = math.sin(-1*2*math.pi*self._frequency/self._sample_rate + self._phase)
        self.cos_omega_t = 2*math.cos(2*math.pi * self._frequency /self._sample_rate)

    def gen_buffer(self, buffer_size):
        #takes in a buffer of any size in the form of nparray
        self.buffer = np.arange(0,buffer_size)
        result = np.zeros(buffer_size)
        self._phase = self._phase % (2*math.pi)

        for i in range(buffer_size):

            x = self.cos_omega_t*self.states[1] - self.states[0]
            result[i] = float(self._amplitude * x)
            self.states[0] = self.states[1]
            self.states[1] = x

            a =  i % 5
            
            if a == 0 :
                print("hello")
                self._frequency += 10
    

        result = result/np.max(result)
        
        self.cal_phase()

        return result


