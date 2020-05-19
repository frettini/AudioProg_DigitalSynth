from PyQt5.QtCore import QIODevice, QByteArray
from PyQt5.QtMultimedia import QAudioFormat
import numpy as np

class Meep(QIODevice):
    
    SAMPLES_PER_READ = 2048
    
    def __init__(self, format, activeGen, parent = None):

        QIODevice.__init__(self, parent)
        self.data = QByteArray()
        
        # Preserve phase across calls
        self.phase = 0
        self.freq = 440

        self.generator = activeGen

        self.convert_16_bit = float(2**15)

        # Check we can deal with the supplied
        # sample format. We're supposed to be
        # able to deal with any requested
        # sample format. But this is a
        # _minimal_ example, right?
        if format.isValid() and \
           format.sampleSize() == 16 and \
           format.byteOrder() == \
                QAudioFormat.LittleEndian and \
           format.sampleType() == \
                QAudioFormat.SignedInt and \
           format.channelCount() == 1 :
               print(
                 "Meep: Format compatible. Good."
               )
               self.format = format
    
    
    def start(self):
        
        # Call QIODevices open
        # making this object readable
        self.open(QIODevice.ReadOnly)
    

    def generateData(self, format, samples):
        
        result_buffer = self.generator.genBuffer(samples)
        result_buffer = np.int16( result_buffer * (self.convert_16_bit-1) )
        return result_buffer.tostring()

    
    def readData(self, bytes):

        if bytes > 2 * Meep.SAMPLES_PER_READ:
            bytes = 2 * Meep.SAMPLES_PER_READ
        return self.generateData(self.format,
                                 bytes//2)