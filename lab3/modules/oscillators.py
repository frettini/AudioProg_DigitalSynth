import math

import numpy as np
from modules import oscillator
from scipy import signal


class SineOscillator(oscillator.Oscillator):
    
    def math_osc(self):
        return self.amplitude * np.sin(self.time/self.sample_rate * 2*math.pi * self.frequency + self.offset)


class SawOscillator(oscillator.Oscillator):
    
    def math_osc(self):
        return self.amplitude * signal.sawtooth(2 * math.pi * self.frequency * self.time/self.sample_rate + self.offset)

class SquareOscillator(oscillator.Oscillator):

    def math_osc(self):
        return self.amplitude *signal.square(2 * np.pi * self.frequency * self.time/self.sample_rate + self.offset)
