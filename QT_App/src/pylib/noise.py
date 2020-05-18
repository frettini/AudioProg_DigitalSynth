# needed to import a module when it is not contained within a package
# used now as the swig filter is maintained at a top level
# might be better to wrap the application in a pacakge or move swig_fitler with the modules

from .gen import Generator
import scipy.signal
import numpy as np
import math


import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

import filter_ext.swig_filter as sf


# White Noise Generator
# White noise created from the numpy random method
class WhiteNoise(Generator):

    def __init__(self, sample_rate = 44100):
        self.mean = 0
        self.std = 0

    def genBuffer(self, bufferSize):

        if bufferSize == 0:
            bufferSize = 2048

        result =  np.random.standard_normal(size=bufferSize)

        return result 

    def setFreq(self, freq):
        return 0


# Flute like generator, combines the White Noise and Filter Classes
class FilteredNoise(Generator):

    def __init__(self, freq = 440, sample_rate = 44100):
        self._sampleRate = sample_rate
        self._frequency = freq

        self.gpass = 9
        self.gstop = 10
        self.bw = 50

        # init filterchain and white noise gen
        # give init coefficients
        self.wn = WhiteNoise()
        self.fc = sf.FilterChain(self.getCoef())
        
    def genBuffer(self, bufferSize):

        if bufferSize == 0:
            bufferSize = 2048
        # shows the biggest flaw of this design! 
        # the white noise and filter chain have different arguments for the function
        resultBuf = np.zeros(bufferSize)
        self.fc.modBuffer(resultBuf, self.wn.genBuffer(bufferSize))

        try:
            norm_result = resultBuf/np.max(resultBuf)
        except ValueError:
            norm_result = resultBuf
        return norm_result 


    
    def setFreq(self, freq):
        self._frequency = freq
        self.fc.setCoef(self.getCoef())

    # calculate IIR coefficients
    def getCoef(self):
        wp = [self._frequency*2/self._sampleRate, (self._frequency+1)*2/self._sampleRate ]    # multiply by two for nyquist frequency
        ws = [(self._frequency-self.bw)*2/self._sampleRate, (self._frequency-self.bw)*2/self._sampleRate ]
        coefs = scipy.signal.iirdesign(wp,ws,self.gpass,self.gstop,output='sos', ftype='ellip')
        return coefs

    def setQ(self, gstop):
        if gstop > 100:
            self.gstop = 100
        elif gstop < 10:
            self.gstop = 10
        else:
            self.gstop = gstop

        self.setFreq(self._frequency)

if __name__ == "__main__":

    import scipy.fftpack
    import matplotlib.pyplot as plot

    fn = FilteredNoise()

    result = fn.genBuffer(2048)
    print(fn._sampleRate)

    norm_result = result/np.max(abs(result)) # normalize result (avoid blown filters)
    result_freq = scipy.fftpack.fft(norm_result) # get spectrum
    
    _frequency = 400
    _sampleRate= 44100
    gpass = 9
    gstop= 100

    # starts with 3 filters

    wp = [_frequency*2/_sampleRate, (_frequency+1)*2/_sampleRate ]    # multiply by two for nyquist frequency
    ws = [(_frequency-25)*2/_sampleRate, (_frequency-25)*2/_sampleRate ]
    coefs = scipy.signal.iirdesign(wp,ws,gpass,gstop,output='sos', ftype='ellip')
    print(coefs)

    fc = sf.FilterChain(coefs)

    #removes one filter

    wp = [_frequency*2/_sampleRate, (_frequency+1)*2/_sampleRate ]    # multiply by two for nyquist frequency
    ws = [(_frequency-50)*2/_sampleRate, (_frequency-50)*2/_sampleRate ]
    coefs = scipy.signal.iirdesign(wp,ws,gpass,gstop,output='sos', ftype='ellip')
    print(coefs)

    fc.setCoef(coefs)

    # adds one filter

    wp = [_frequency*2/_sampleRate, (_frequency+1)*2/_sampleRate ]    # multiply by two for nyquist frequency
    ws = [(_frequency-25)*2/_sampleRate, (_frequency-25)*2/_sampleRate ]
    coefs = scipy.signal.iirdesign(wp,ws,gpass,gstop,output='sos', ftype='ellip')
    print(coefs)
    
    fc.setCoef(coefs)


    print("Alles ist gut")


    # plot.plot(np.real(result_freq))
    # plot.plot(np.imag(result_freq))
    # plot.show()


