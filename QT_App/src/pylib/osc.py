import numpy as np
import math

from .gen import Generator

class RecOsc(Generator):
    """
    Cosine tone generator using recursive oscillatory techniques.

    Accepts an optional initial frequency and sample rate. The frequency is then
    set using a getter/setter or setFreq. The buffer is generated thanks the 
    genBuffer method. The phase is calculated and maintained between each buffer
    and at each frequency change using calPhase.
    """


    def __init__(self,  freq = 440, sample_rate = 44100):
        
        super().__init__(sample_rate)
        
        self._phase = 0
        self._frequency = freq
        self.states = np.zeros(2)

        # initialize the delayed samples with preliminary sine values
        self.states[1] = math.sin(-1*2*math.pi*freq/sample_rate)
        self.states[0] = math.sin(-2*2*math.pi*freq/sample_rate)
        self.cos_omega_t = 2*math.cos(2*math.pi * freq /sample_rate)

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, value):
        # check the validity of the frequency value and update it
        if value >= 0 or value <= self._sampleRate/2:
            self.setFreq(value)
            
        elif value > self._sampleRate/2:
            self.setFreq(self._sampleRate/2)
        else:
            self._frequency = 0
    
    def calPhase(self):
        # calculate and return the phase of the generator
        
        phase = np.arcsin(self.states[1])

        if self.states[1] > self.states[0]:
            #going up
            self._phase = phase

        elif self.states[1] < self.states[0] :
            #going down
            self._phase = np.pi - phase

    def setFreq(self, freq):
        """ 
        Updates the generator's frequency and recalculates states to ensure phase continuity.
        """
        self._frequency = freq
        
        # recalculate the two previous samples with the new freq and phase
        self.states[0] = math.sin(-1*2*math.pi*self._frequency/self._sampleRate + self._phase)
        self.cos_omega_t = 2*math.cos(2*math.pi * self._frequency /self._sampleRate)


    def genBuffer(self, buffer_size, end_freq = 0):
        """ Return an array of size bufferSize containing audio samples. """
        
        #if given buffer size is 0 default to 2048
        if buffer_size <= 0:
            buffer_size = 2048

        
        self.buffer = np.arange(0,buffer_size)
        result = np.zeros(buffer_size)
        self._phase = self._phase % (2*math.pi)
        chirp = False
        
        if end_freq == 0:
            end_freq = self._frequency
        
        # if an end frequency is given, produce a chirp
        if end_freq != self._frequency:
            step = (end_freq - self._frequency)/buffer_size
            chirp = True

        #generate recursive samples in the buffer
        for i in range(buffer_size):

            x = self.cos_omega_t*self.states[1] - self.states[0]
            result[i] = float(x)
            self.states[0] = self.states[1]
            self.states[1] = x

            #if end_freq is different, step the frequency
            if chirp == True and i > 2:
                
                self.calPhase()
                self.setFreq(self._frequency + step)
                
        # normalize the result
        norm_result = result/np.max(result)
        
        self.calPhase()

        return norm_result


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

