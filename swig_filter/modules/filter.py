from .gen import Gen
import numpy as np
from .delay import Delay
from .complexcal import ComplexCal

# IIR Filter Class
class Filter(Gen):

    # initialize with zeros and poles, if using coefficients 
    def __init__(self, pole_mag, pole_ang, zero_mag, zero_ang):
        self.c  = ComplexCal()
        self.a = np.zeros(3)
        self.b = np.zeros(3)
        self.set_p_a_z(pole_mag, pole_ang, zero_mag, zero_ang)

    # compute coefficients, given poles and zeros
    def set_p_a_z(self, pole_mag, pole_ang, zero_mag, zero_ang):
        x_z , y_z = self.c.polar_to_cart(zero_mag, zero_ang)
        x_p , y_p = self.c.polar_to_cart(pole_mag, pole_ang)

        self.a[0] = 1
        self.a[1] = -2*x_z 
        self.a[2] = x_z**2 + y_z**2
        self.b[0] = 1
        self.b[1] = -2*x_p
        self.b[2] = x_p**2 + y_p**2
        self.gain = 1
        self.d = Delay(10,2)

    # set coefficients directly
    def setcoef(self, coefs):
        self.a = coefs[0:3]
        self.b = coefs[3:6]

    def gen_buffer(self, buffer):
        result = np.zeros(len(buffer))
        
        for i in range(len(buffer)):
            middle = buffer[i] - self.b[1] * self.d.process_arr[0] - self.b[2] * self.d.process_arr[1] 
            result[i] = middle * self.a[0] + (self.a[1])*self.d.process_arr[0] + (self.a[2])*self.d.process_arr[1]
            self.d.process(middle)
        return result