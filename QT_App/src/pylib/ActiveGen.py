from PyQt5.QtCore import pyqtSlot
import numpy as np

from gen import Generator
import osc, modifiers, noise


# The currently active generator
# This is an interface Class to communicate with the Meep and view
class ActiveGen(Generator):

    # initialize all the generators 
    # initialize all the modifiers
    def __init__(self, freq=440, sampleRate = 44100):
        self._frequency = freq

        self.recOsc = osc.RecOsc(self._frequency)
        self.wNoise = noise.WhiteNoise(self._frequency)
        self.fNoise = noise.FilteredNoise(self._frequency)
        
        self.master = modifiers.Gain(1)
        
        self.activeGen = self.recOsc

    # generate buffer using the active generator
    def genBuffer(self, bufferSize):
        return self.modBuffer(self.activeGen.genBuffer(bufferSize))

    # apply modifiers contained in the class
    def modBuffer(self, inBuffer):
        return self.master.modBuffer(inBuffer)

    # set Frequency of the generator currently in use
    def setFreq(self, freq = 440):
        self._frequency= freq
        self.activeGen.setFreq(self._frequency)
        
    # probably not the best way of doing it,
    # I could put it in a dictionary, just test for now
    def setActive(self, index):
        if index == 0:
            self.activeGen = self.recOsc    
        elif index == 1:
            self.activeGen = self.wNoise
        elif index == 2:
            self.activeGen = self.fNoise

        self.setFreq(self._frequency)

    

if __name__ == "__main__":

    import matplotlib.pyplot as plot

    ag = ActiveGen()

    result = np.zeros(6000)
    result[:2000] = ag.genBuffer(2000)
    ag.setFreq(220)
    result[2000:4000] = ag.genBuffer(2000)
    ag.setActive(2)
    result[4000:] = ag.genBuffer(2000)

    plot.plot(result)
    plot.show()
