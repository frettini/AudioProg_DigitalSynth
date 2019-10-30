import numpy as np

class Delay:

    def __init__(self, nsamp_delay):
        self.n = nsamp_delay
        self.delay_store = np.zeros(nsamp_delay)
        self.delay_inter = np.zeros(nsamp_delay)

    def delay(self, input_arr):

        try:
            
            self.delay_inter = input_arr[-self.n:]
            print( self.delay_store)
            print(input_arr[:-self.n])
            input_arr = np.concatenate((self.delay_store, input_arr[:-self.n]))
           
            self.delay_store = self.delay_inter

            return input_arr

        except IndexError:
            print("IndexError : input array smaller than delay, return Input Array")
            return input_arr
    


class Gain:

    def __init__(self, gain):
        self.gain = gain
        

    def scale(self, input_arr):
        return  input_arr * self.gain







