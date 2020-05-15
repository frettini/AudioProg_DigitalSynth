from PyQt5.QtCore import pyqtSlot
import numpy as np

from .gen import Generator
from .osc import RecOsc
from .modifiers import Gain, ADSR
from .noise import WhiteNoise, FilteredNoise


# The currently active generator
# This is an interface Class to communicate with the Meep and view
class ActiveGen(Generator):

    # initialize all the generators 
    # initialize all the modifiers
    def __init__(self, freq=440, sampleRate = 44100):
        self._frequency = freq

        self.recOsc = RecOsc(self._frequency)
        self.wNoise = WhiteNoise(self._frequency)
        self.fNoise = FilteredNoise(self._frequency)
        self.genLst = [self.fNoise, self.recOsc, self.wNoise]

        self.master = Gain(1)
        self.adsr = ADSR(2048)
        
        
        self.activeGen = self.genLst[0]

    # generate buffer using the active generator
    def genBuffer(self, bufferSize):
        return self.modBuffer(self.activeGen.genBuffer(bufferSize))

    # apply modifiers contained in the class
    def modBuffer(self, inBuffer):
        outBuffer = self.adsr.modBuffer(inBuffer)
        return self.master.modBuffer(outBuffer)

    # set Frequency of the generator currently in use
    def setFreq(self, freq):
        # change frequency only if necessary
        if freq != self._frequency:
            self._frequency= freq
            self.activeGen.setFreq(self._frequency)

            
    # set active generator, make sure the index matches the sliders
    # to ensure knowledge of view is not required,a dictionary is best
    def setActive(self, index):
        self.activeGen = self.genLst[index]
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
