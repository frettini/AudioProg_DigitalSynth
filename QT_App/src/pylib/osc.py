import numpy as np
import math

from .gen import Generator

# recursive oscillator done using the power of physics
class RecOsc(Generator):


    def __init__(self,  freq = 440, amp = 1, sample_rate = 44100):
        
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
        if value >= 0 or value <= self._sampleRate/2:
            self.setFreq(value)
            
        elif value > self._sampleRate/2:
            self.setFreq(self._sampleRate/2)
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

    def setFreq(self, freq):
        self._frequency = freq
        #need to recalculate the two previous samples with the new freq and phase
        self.states[0] = math.sin(-1*2*math.pi*self._frequency/self._sampleRate + self._phase)
        self.cos_omega_t = 2*math.cos(2*math.pi * self._frequency /self._sampleRate)


    def genBuffer(self, buffer_size, end_freq = 0):
        #takes in a buffer of any size in the form of nparray
        if end_freq == 0:
            end_freq = self._frequency
        
        self.buffer = np.arange(0,buffer_size)
        result = np.zeros(buffer_size)
        self._phase = self._phase % (2*math.pi)
        chirp = False
        
        if end_freq != self._frequency:
            step = (end_freq - self._frequency)/buffer_size
            chirp = True

        #generate recursive samples in the buffer
        for i in range(buffer_size):

            x = self.cos_omega_t*self.states[1] - self.states[0]
            result[i] = float(self._amplitude * x)
            self.states[0] = self.states[1]
            self.states[1] = x

            #if end_freq is different, step the frequency
            if chirp == True and i > 2:
                
                self.cal_phase()
                self.setFreq(self._frequency + step)
                
    
        
        result = result/np.max(result)
        
        self.cal_phase()

        return result


if __name__ == "__main__":

    import matplotlib.pyplot as plot
    import time

    ro = RecOsc()

    result = np.zeros(4096)
    
    #takes about 3 ms to generate a buffer which should be manageable
    #if not, it will have to be implemented in c++ 
    start = time.time()
    result[:2048] = ro.genBuffer(2048)
    end = time.time()
    print("time taken: {}".format(end - start))
    
    ro.setFreq(220)
    result[2048:] = ro.genBuffer(2048)

    plot.plot(result)
    plot.show()

