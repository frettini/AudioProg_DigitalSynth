from .gen import Gen
import numpy as np
from .delay import Delay
from .complexcal import ComplexCal

# IIR Filter Class
class Filter(Gen):

    # initialize with zeros and poles, if using coefficients 
    def __init__(self, pole_mag, pole_ang, zero_mag, zero_ang):
        self.c  = ComplexCal()
        self.set_p_a_z(pole_mag, pole_ang, zero_mag, zero_ang)

    def set_p_a_z(self, pole_mag, pole_ang, zero_mag, zero_ang):
        x_z , y_z = self.c.polar_to_cart(zero_mag, zero_ang)
        x_p , y_p = self.c.polar_to_cart(pole_mag, pole_ang)

        self.a0 = 1
        self.a1 = -2*x_z 
        self.a2 = x_z**2 + y_z**2
        self.b1 = -2*x_p
        self.b2 = x_p**2 + y_p**2
        self.gain = 1
        self.d = Delay(10,2)

    def setcoef(self, a0,a1,a2,b0,b1,b2):
        self.a0 = a0
        self.a1 = a1
        self.a2 = a2
        self.b0 = b0
        self.b1 = b1
        self.b2 = b2

    def gen_buffer(self, buffer):
        result = np.zeros(len(buffer))
        
        for i in range(len(buffer)):
            middle = buffer[i] - self.b1 * self.d.process_arr[0] - self.b2 * self.d.process_arr[1] 
            result[i] = middle * self.a0 + (self.a1)*self.d.process_arr[0] + (self.a2)*self.d.process_arr[1]
            self.d.process(middle)
        return result