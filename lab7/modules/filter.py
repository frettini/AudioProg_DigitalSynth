import numpy as np
from .delay import Delay
from .complexcal import ComplexCal

class Filter():

    def __init__(self, pole_mag, pole_ang, zero_mag, zero_ang):
        self.c  = ComplexCal()
        x_z , y_z = self.c.polar_to_cart(zero_mag, zero_ang)
        x_p , y_p = self.c.polar_to_cart(pole_mag, pole_ang)

        self.a1 = 2*x_z 
        self.a2 = x_z**2 + y_z**2
        self.b1 = 2*x_p
        self.b2 = x_p**2 + y_p**2
        self.gain = 1
        self.d = Delay(10,2)


    def filtering(self, buffer):
        result = np.zeros(len(buffer))
        for i in range(len(buffer)):
            result[i] = buffer[i] + (self.a1-self.b1)*self.d.process_arr[0] + (self.a2 - self.b2)*self.d.process_arr[1]
           # (1+self.a1*self.d.process_arr[0]+self.a2*self.d.process_arr[1])/(1+self.b1*self.d.process_arr[0]+self.b2*self.d.process_arr[1])
            self.d.process(buffer[i])
        return result 