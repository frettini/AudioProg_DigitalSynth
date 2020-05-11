import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
import swig_filter as sf
import numpy as np

# Delay Class implemented using Python 
# another Delay class is implemented in c++ and is more efficient
class PyDelay:

    def __init__(self, nsamp_delay, process_delay):
        self.n = nsamp_delay
        self.delay_store = np.zeros(nsamp_delay)
        self.delay_inter = np.zeros(nsamp_delay)
        self.process_arr = np.zeros(process_delay)

    def delay(self, input_arr):

        try:
            
            self.delay_inter = input_arr[-self.n:]
            input_arr = np.concatenate((self.delay_store, input_arr[:-self.n]))
           
            self.delay_store = self.delay_inter

            return input_arr

        except IndexError:
            print("IndexError : input array smaller than delay, return Input Array")
            return input_arr

    def process(self, audio_sample):
        self.process_arr = np.concatenate(([audio_sample], self.process_arr[:(len(self.process_arr)-1)]))
        return self.process_arr


# Simple Gain Class that multiplies buffer with a set value
class Gain(sf.Modifier):

    def __init__(self, gain):
        self.setGain(gain)
        
    def setGain(self, gain):
        self.gain = gain

    def modBuffer(self, input_arr):
        return  input_arr * self.gain


# ADSR envelope Mod
class ADSR(sf.Modifier):

    def __init__(self):
        pass

    def modBuffer(self, input_arr):
        pass

if __name__ == "__main__":

    d = PyDelay(10, 10)
    d.process(1)
    d.process(2)
    print(d.process_arr)

    g = Gain(2)
    print(g.modBuffer(d.process_arr))



