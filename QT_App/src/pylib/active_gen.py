from PyQt5.QtCore import pyqtSlot
import numpy as np

from .gen import Generator
from .osc import RecOsc
from .modifiers import Gain, ADSR_V2
from .noise import WhiteNoise, FilteredNoise


# The currently active generator
# This is an interface Class to communicate with the Meep and view
class ActiveGen(Generator):
    """
    Generator which contains multiple generators and enables selection between them.

    Contains the usual generator methods such as genBuffer to generate a buffer and
    setFreq to set the generator's frequency. Those methods call the genBuffer and 
    setFreq of the generator contained in the activeGen variable. The active generator
    can be changed using the setActive method.
    """

    def __init__(self, freq=440, sampleRate = 44100, samplePerRead = 2048):
        self._frequency = freq

        # initialise all the generators
        self.recOsc = RecOsc(self._frequency)
        self.wNoise = WhiteNoise(self._frequency)
        self.fNoise = FilteredNoise(self._frequency)
        # store the generators in a list
        self.genLst = [self.fNoise, self.recOsc, self.wNoise]

        # initialise all the modifiers
        self.master = Gain(1)
        self.adsr = ADSR_V2(2048)
        
        # set the active generator with a initial generator value
        self.activeGen = self.genLst[0]


    def genBuffer(self, bufferSize):
        """ 
        Return an array of size bufferSize containing audio samples generated
        from the active generator. The modifiers affect the buffer using the modBuffer method 
        """
        return self.modBuffer(self.activeGen.genBuffer(bufferSize))

    # apply modifiers contained in the class
    def modBuffer(self, inBuffer):
        """
        Returns the modified input array. Each modifier is called here and modify
        the buffer one at a time using their own modBuffer
        """
        outBuffer = self.adsr.modBuffer(inBuffer)
        return self.master.modBuffer(outBuffer)

    def setFreq(self, freq):
        """ 
        Updates the active generator's frequency using its own setFreq.
        freq is the new frequency which has to be between 0 and the nyquist frequency
        """
        # change frequency only if necessary
        if freq != self._frequency:
            self._frequency= freq
            self.activeGen.setFreq(self._frequency)

            
    # set active generator, make sure the index matches the sliders
    # to ensure knowledge of view is not required,a dictionary is best
    def setActive(self, index):
        """
        Set the active generator.
        index is an integer which accesses the generator list
        """
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
