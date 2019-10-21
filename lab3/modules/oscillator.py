import numpy as np
import math
from scipy import signal

class Oscillator:
    
    def __init__(self, buffer_size = 2048, sample_rate = 44100):
        self.buffer_size = buffer_size
        self.sample_rate = sample_rate
        
        self.buffer_start = 0
        self.buffer_stop = 0
        self.frequency = 0
        self.amplitude = 0.0
        self.offset= 0
        self.phase = 0
        self.result = np.zeros(buffer_size)

        self.last_samples = np.zeros(2)
        

    def math_osc(self):
        return None

    def calculate_phase(self):
        
        


    def gen_wave(self ,sample_count = 0, buffer_input = None):
        #buffer_size : specifies the size of the "wave" or buffer
        #offset: default 0, specifies the offset
        #amplitude: default 1, specifies the amplitude of the added wave 

        self.buffer_stop = self.buffer_start+self.buffer_size

        
        self.buffer = np.arange(self.buffer_start, self.buffer_stop)
        self.offset = self.offset % (2*math.pi)
        #generate sine wave, control amplitude by multiplication, add to existing result (ie buffer_input if there is one)
        mathosc = self.math_osc()
        print(mathosc[:2])
        

        self.result = mathosc 
        
        #normalize result by dividing by the maximum of the string
        self.result = self.result/np.max(self.result)
        print(self.result[:2])

        self.last_samples = self.result[-2:]
        self.offset = self.calculate_phase()

        return self.result


class SineOscillator(Oscillator):
    
    def math_osc(self):
        x = ((self.buffer * 2*math.pi * self.frequency)/self.sample_rate) % (2*math.pi)
        return self.amplitude * np.sin(x + self.offset)


class SawOscillator(Oscillator):
    
    def math_osc(self):
        return self.amplitude * signal.sawtooth(2 * math.pi * self.frequency * self.buffer/self.sample_rate + self.offset)

class SquareOscillator(Oscillator):

    def math_osc(self):
        return self.amplitude * signal.square(2 * np.pi * self.frequency * self.buffer/self.sample_rate + self.offset)

        

