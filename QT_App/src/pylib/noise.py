import scipy.signal
import numpy as np
import math

from .gen import Generator
from ..filter_ext import swig_filter as sf


class WhiteNoise(Generator):
    """
    White Noise generator using the numpy random function.

    Accepts an optional initial sample rate. The buffer is generated thanks the 
    genBuffer method. The set frequency exists but returns 0.
    """

    def __init__(self, sample_rate = 44100):
        self.mean = 0
        self.std = 0

    def genBuffer(self, bufferSize):
        """ Return an array of size bufferSize containing audio samples """
        
        # check if the buffer size is invalid
        if bufferSize <= 0:
            bufferSize = 2048

        result =  np.random.standard_normal(size=bufferSize)

        return result 

    def setFreq(self, freq):
        return 0


# Flute like generator, combines the White Noise and Filter Classes
class FilteredNoise(Generator):
    """
    Filtered Noise generator using the filter extension found in the 
    filter_ext package and the White Noise generator.

    Accepts an optional initial sample rate and frequency. The buffer is generated thanks the 
    genBuffer method. The set frequency exists but returns 0. The frequency is 
    updated by recalculating the filters' coefficients using the getCoef method.
    The sharpness of the filter is updated using the setQ method.
    """

    def __init__(self, freq = 440, sample_rate = 44100):
        self._sampleRate = sample_rate
        self._frequency = freq

        self.gpass = 9
        self.gstop = 10
        self.bw = 1

        # init filterchain and white noise gen
        # give init coefficients
        self.wn = WhiteNoise()
        self.fc = sf.FilterChain(self.getCoef())
        
    def genBuffer(self, bufferSize):
        """ Return an array of size bufferSize containing audio samples. """
        
        # check if the buffer size is invalid
        if bufferSize <= 0:
            bufferSize = 2048

        # generate the buffer using the white noise instance
        # modify it using the filter chain
        resultBuf = np.zeros(bufferSize)
        self.fc.modBuffer(resultBuf, self.wn.genBuffer(bufferSize))

        return resultBuf/np.max(resultBuf)

    def setFreq(self, freq):
        """ 
        Updates the generator's frequency and recalculates the filters' coefficients.
        """
        self._frequency = freq
        self.fc.setCoef(self.getCoef())

    # calculate IIR coefficients
    def getCoef(self, freq = 0):
        """
        Updates the filters' iir coffecients using the scipy iirdesign method
        """
        if freq != 0:
            self._frequency = freq
        
        wp = [self._frequency*2/self._sampleRate, (self._frequency+self.bw)*2/self._sampleRate ]    # multiply by two for nyquist frequency
        ws = [(self._frequency-50)*2/self._sampleRate, (self._frequency-50)*2/self._sampleRate ]
        coefs = scipy.signal.iirdesign(wp,ws,self.gpass,self.gstop,output='sos', ftype='ellip')
        return coefs

    def setQ(self, bw):
        """
        Update the sharpness of the filter by taking the gstop value and resetting the frequency.
        """
        if gstop > 100:
            self.bw = 100
        elif gstop < 10:
            self.bw = 1
        else:
            self.bw = bw

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


