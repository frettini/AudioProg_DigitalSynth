import os,sys,inspect
import numpy as np

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
import filter_ext.swig_filter as sf

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

    def __init__(self, samplePerRead, sampleRate = 44100, A=0.1, D=0.1, S=0.7, R=1.0):
        self.noteOn = False
        self.index = 0
        self.sampleRate = sampleRate
        self.samplePerRead = samplePerRead

        self.maxA = int(1 * self.sampleRate)
        self.maxD = int(1 * self.sampleRate)
        self.maxR = int(2 * self.sampleRate)
        self.setS(S)

        # calculate the maximum size of the Attack and Delay Buffer
        # Make sure it is a multiple of the sample per read rate
        ADmaxsize = self.maxA + self.maxD 
        ADmaxsize += (self.samplePerRead - ADmaxsize % self.samplePerRead)
        self.ADbuffer = np.full(ADmaxsize,self.S)
        print(ADmaxsize)

        # same but for the release buffer
        Rmaxsize = self.maxR
        Rmaxsize += (self.samplePerRead - Rmaxsize % self.samplePerRead)
        self.Rbuffer = np.full(Rmaxsize,self.S)
        print(Rmaxsize)

        # set the buffer values and sustain
        self.setAD(A, D)
        self.setR(R)


    def modBuffer(self, input_arr):
        
        # this could be done by allocating the buffers to an active buffer
        # however this require more memory allocation
        # could also implement the active buffer in the setNote method
        if self.noteOn is True:
            
            # if the note is maintained further than the attack and delay
            # multiply the input value with the sustain value
            if self.index >= len(self.ADbuffer):
                return input_arr*self.S

            result_buffer = input_arr * self.ADbuffer[self.index:(self.index+self.samplePerRead)]
            self.index += self.index+self.samplePerRead
            return result_buffer

        else:
            # if the note is maintained further than the release
            # multiply the input value with 0
            if self.index >= len(self.Rbuffer):
                return input_arr*0.01

            result_buffer = input_arr * self.Rbuffer[self.index:(self.index+self.samplePerRead)]
            self.index += self.index+self.samplePerRead
            return result_buffer
            
        return input_arr

    #generate the buffer for the attack and decay
    def setAD(self, A, D):
        if A <= self.maxA:
            self.A = int(A * self.sampleRate)
        else:
            self.A = self.maxA

        if D <= self.maxD:
            self.D = int(D * self.sampleRate)
        else:
            self.D = self.maxD

        # set frames for A, D, and extra sustain 
        self.ADbuffer[0:self.A] = np.linspace(0,1,self.A)
        self.ADbuffer[self.A:self.A + self.D ] = np.linspace(1, self.S, self.D)
        self.ADbuffer[self.A + self.D:] = self.S


    #generate the buffer for the release
    def setR(self, R):
        if R <= self.maxR:
            self.R = int(R * self.sampleRate)
        else:
            self.R = self.maxR

        self.Rbuffer[0:self.R] = np.linspace(self.S,0.01,self.R)
        self.Rbuffer[self.R:] = 0.01

    def setS(self, S):
        if S <= 1:
            self.S = S
        else:
            self.S = 1

    def setNote(self):
        self.noteOn = not self.noteOn
        self.index = 0


if __name__ == "__main__":

    import matplotlib.pyplot as plot

    d = PyDelay(10, 10)
    d.process(1)
    d.process(2)
    print(d.process_arr)

    g = Gain(2)
    print("Gain modifier")
    print(g.modBuffer(d.process_arr))

    adsrmod = ADSR(20, 60)

    plot.plot(np.concatenate((adsrmod.ADbuffer,adsrmod.Rbuffer)))
    plot.show()



