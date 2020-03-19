SAMPLE_RATE = 44100
AUDIO_CHANS = 1
SAMPLE_SIZE = 16
CTRL_INTERVAL = 100 # milliseconds of audio

import sys
import numpy as np
from PyQt5.QtCore import QByteArray, QIODevice
from PyQt5.QtMultimedia import QAudioFormat, \
                               QAudioOutput
from PyQt5.QtWidgets import QApplication, \
                            QWidget

class Meep(QIODevice):
    
    SAMPLES_PER_READ = 1024
    
    def __init__(self, format, parent = None):

        QIODevice.__init__(self, parent)
        self.data = QByteArray()
        
        # Preserve phase across calls
        self.phase = 0
        
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
        
        #pps controls the frequency
        pps = 440*2*np.pi/format.sampleRate()
        finalphase = samples*pps + self.phase
        tone = (
          10000 * np.sin(
            np.arange(self.phase,
                      finalphase,
                      pps)
          )
        ).astype(np.int16)
        
        self.phase = finalphase % (2*np.pi)
        return tone.tostring()
    
    
    def readData(self, bytes):

        if bytes > 2 * Meep.SAMPLES_PER_READ:
            bytes = 2 * Meep.SAMPLES_PER_READ
        return self.generateData(self.format,
                                 bytes//2)


class ToneGenerator(QWidget):
    
    def __init__(self, parent=None):
        
        QWidget.__init__(self, parent)

        format = QAudioFormat()
        format.setChannelCount(AUDIO_CHANS)
        format.setSampleRate(SAMPLE_RATE)
        format.setSampleSize(SAMPLE_SIZE)
        format.setCodec("audio/pcm")
        format.setByteOrder(
            QAudioFormat.LittleEndian
        )
        format.setSampleType(
            QAudioFormat.SignedInt
        )

        self.output = QAudioOutput(format, self)
        output_buffer_size = \
            int(2*SAMPLE_RATE \
                 *CTRL_INTERVAL/1000)
        self.output.setBufferSize(
            output_buffer_size
        )
        
        self.generator = Meep(format, self)        
        self.generator.start()
        self.output.start(self.generator)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = ToneGenerator()
    window.show()
    sys.exit(app.exec_())