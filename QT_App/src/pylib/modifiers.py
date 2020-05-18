import os,sys,inspect
import numpy as np
from abc import ABC, abstractmethod

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
        self.maxR = int(4 * self.sampleRate)
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
                return input_arr*0

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

        self.Rbuffer[0:self.R] = np.linspace(self.S,0,self.R)
        self.Rbuffer[self.R:] = 0

    def setS(self, S):
        if S <= 1:
            self.S = S
        else:
            self.S = 1

    def setNote(self):
        self.noteOn = not self.noteOn
        self.index = 0

#-------------------------------------------------------------------
# Second implementation of ADSR using a State Machine
#-------------------------------------------------------------------
class ADSRState(ABC):
    def __init__(self, sampleRate, samplePerRead):
        self.sampleRate = sampleRate
        self.samplePerRead = samplePerRead

    # generate the buffer of values
    @abstractmethod
    def process(self, amplitude):
        pass

    # time: time in seconds for each steps
    # internally steps the amplitude step for the state
    @abstractmethod
    def setTime(self, time):
        pass

class AState(ADSRState):
    
    def __init__(self, sampleRate, samplePerRead, time=1):
        super().__init__(sampleRate, samplePerRead)
        self.setTime(time)

    def process(self, amp):
        # calculate the amplitude we want to get to
        newAmp = amp + self.step
        # if it is higher thank 1, clamp and set the next state to decay        
        if newAmp >= 1:
            newAmp = 1
            nextState = "decay"
        else:
            nextState = "attack"
        
        # generate the buffer
        result = np.linspace(amp, newAmp, self.samplePerRead)

        return newAmp, nextState, result

    def setTime(self, time):
        self.step = self.samplePerRead / (self.sampleRate*time) 
        print("A: " + str(self.step))



class DState(ADSRState):
    
    def __init__(self, sampleRate, samplePerRead, time=1, sustain=0.7):
        super().__init__(sampleRate, samplePerRead) 
        self.sustain = sustain
        self.setTime(time, self.sustain)

    def process(self, amp):
        newAmp = amp + self.step

        if newAmp < self.sustain:
            newAmp = self.sustain
            nextState = "sustain"
        else:
            nextState = "decay"

        result = np.linspace(amp, newAmp, self.samplePerRead)

        return newAmp, nextState, result

    def setTime(self, time, sustain):
        self.step = self.samplePerRead * (self.sustain - 1)/(self.sampleRate * time)
        print("D: " + str(self.step))



class SState(ADSRState):
    
    def __init__(self, sampleRate, samplePerRead, sustain=0.7):
        super().__init__(sampleRate, samplePerRead)
        self.setSustain(sustain)

    def process(self, amplitude):
        newAmp = self.sustain
        nextState = "sustain"
        result = np.full(self.samplePerRead, self.sustain)
        return newAmp, nextState, result

    # needs a reference to the sustain value of the DState
    # or it is taken care of in the ADSR class
    def setSustain(self, sustain):
        if sustain > 1:
            self.sustain = 1
        elif sustain < 0:
            self.sustain = 0
        else:
            self.sustain = sustain

    def setTime(self, time):
        return 0


class RState(ADSRState):
    
    def __init__(self, sampleRate, samplePerRead, time=2, sustain=0.7):
        super().__init__(sampleRate, samplePerRead)
        self.setTime(time, sustain)

    def process(self, amp):
        newAmp = amp + self.step

        if newAmp < 0 :
            newAmp = 0

        nextState = "release"
        result = np.linspace(amp, newAmp, self.samplePerRead)
        return newAmp, nextState, result

    def setTime(self, time, sustain=0.7):
        self.sustain = sustain
        self.step = self.samplePerRead * (-self.sustain)/(self.sampleRate * time)
        print("R: " + str(self.step))

# ADSR modifier and state manager
class ADSR_V2(sf.Modifier):
    
    def __init__(self, samplePerRead = 2048, sampleRate = 44100, A=1,D=1,S=0.7,R=2):
        self.samplePerRead = samplePerRead
        self.sampleRate = sampleRate
        self.noteOn = False
        self.amplitude = 0.0
        self.R = R
        
        aState = AState(self.sampleRate, self.samplePerRead, A)
        dState = DState(self.sampleRate, self.samplePerRead, D, S)
        sState = SState(self.sampleRate, self.samplePerRead, S)
        rState = RState(self.sampleRate, self.samplePerRead, R, S)

        self.states = {
            "attack"  : aState, 
            "decay"   : dState, 
            "sustain" : sState,
            "release" : rState 
                       }
        
        self.currentState = self.states["release"]

    def modBuffer(self, input_arr):
        
        self.amplitude, nextState, modifier = self.currentState.process(self.amplitude)
        
        if self.currentState != self.states[nextState]:
            self.currentState = self.states[nextState]

        return modifier * input_arr

    def setADSR(self, A, D, S, R):
        self.R = R

        self.states["attack"].setTime(A)
        self.states["decay"].setTime(D, S)
        self.states["sustain"].setSustain(S)
        self.states["release"].setTime(R)


    def setNote(self, status):
        
        self.noteOn = status
        if self.noteOn is True:
            self.currentState = self.states["attack"]

        if self.noteOn is False:
            self.currentState = self.states["release"]
            #ensure equal release time from any amplitude
            self.currentState.setTime(self.R , self.amplitude)



if __name__ == "__main__":

    import matplotlib.pyplot as plot

    d = PyDelay(10, 10)
    d.process(1)
    d.process(2)
    print(d.process_arr)

    g = Gain(2)
    print("Gain modifier")
    print(g.modBuffer(d.process_arr))

    adsrmod = ADSR_V2(20, 60, S=0.2)
    random =  np.random.standard_normal(360)
    result = np.zeros(360)
    
    adsrmod.setNote(True)
    for i in range(0,100,20):
        result[i:i+20] = adsrmod.modBuffer(random[i:i+20])
    adsrmod.setNote(False)
    for i in range(100,140,20):
        result[i:i+20] = adsrmod.modBuffer(random[i:i+20])
    adsrmod.setNote(True)
    for i in range(140,200,20):
        result[i:i+20] = adsrmod.modBuffer(random[i:i+20])
    adsrmod.setNote(False)
    for i in range(200,360,20):
        result[i:i+20] = adsrmod.modBuffer(random[i:i+20])
    

    plot.plot(result)
    plot.show()



