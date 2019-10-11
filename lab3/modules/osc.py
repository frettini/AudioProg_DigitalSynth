import numpy as np
import math
from scipy import signal

class Oscillator:

    def __init__(self):
        self.__frequency = 0
        self.__phase = 0
        self.__amplitude = 0

    def gen_buffer(self):
        pass

    def calculate_phase(self):
        pass


class SineOscillator(Oscillator):

    name = "Sine"

    def gen_buffer(self):
        return "hello world"