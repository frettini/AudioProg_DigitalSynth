
import sys
from PyQt5.QtCore import \
    Qt, pyqtSlot, pyqtSignal, QObject, QThread, QByteArray, QIODevice
from PyQt5.QtWidgets import \
    QApplication, QWidget, \
    QSlider, QPushButton, \
    QMessageBox, \
    QVBoxLayout, QHBoxLayout
from PyQt5.QtMultimedia import QAudioFormat, QAudioOutput

import math
import numpy as np
import mido
import rtmidi
import scipy.signal

from swig_module import swig_filter as sf
from swig_module.modules import white_noise

SAMPLE_RATE = 44100
AUDIO_CHANS = 1
SAMPLE_SIZE = 16
CTRL_INTERVAL = 100 # milliseconds of audio


class ExecutiveToy(QWidget):

    def __init__(self, parent = None):
        super().__init__(parent)
        self.create_UI(parent)




    def create_UI(self, parent):        
        # Create a slider and two buttons
        self.mySlider = QSlider(Qt.Horizontal)
        self.showButton = \
            QPushButton(self.tr('&Show Value'))
        self.quitButton = \
            QPushButton(self.tr('&Quit'))
        
        # No parent: we're going to add this
        # to vLayout.
        hLayout = QHBoxLayout()
        hLayout.addWidget(self.showButton)
        hLayout.addStretch(1)
        hLayout.addWidget(self.quitButton)
        
        # parent = self: this is the
        # "top level" layout
        vLayout = QVBoxLayout(self)
        vLayout.addWidget(self.mySlider)
        vLayout.addWidget(ToneGenerator())
        vLayout.addLayout(hLayout)  

        self.quitButton.clicked.connect(
            self.quitClicked
        )
        self.showButton.clicked.connect(
            self.showClicked
        )

    
    # Now the slots which accept events
    @pyqtSlot()
    def quitClicked(self):
        self.close()
        
    @pyqtSlot()
    def showClicked(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
    
        msg.setText('Current Slider Value')
        msg.setInformativeText(
            'When requested, value was '
            + str(self.mySlider.value())
        )
        msg.setWindowTitle('mySlider')
        msg.setDetailedText('That is all I know')
        msg.setStandardButtons(QMessageBox.Ok)
    	
        msg.exec()




class MidiPortReader(QObject):

    # Create a signal for when a
    # MIDI note_on happens
    newNoteFrequency = pyqtSignal(float)
    
    # Object initialisation:
    def __init__(self):
        QObject.__init__(self)
        mido.set_backend('mido.backends.rtmidi')
        print("Using MIDI APIs: {}".format(mido.backend.module.get_api_names()))
        
    
    # Define a function which is to
    # run in its own thread
    def listener(self):
        with mido.open_input(virtual=False) as mip:
            for mmsg in mip:
                print(mmsg.type)
                print(mmsg.bytes())
        
                # Only communicate via the Qt signal
                # Qt will stop us hurting ourselves
                
                self.newNoteFrequency.emit(float(mmsg.bytes()[1]))
        




class Meep(QIODevice):
    
    SAMPLES_PER_READ = 2048
    
    def __init__(self, format, parent = None):

        QIODevice.__init__(self, parent)
        self.data = QByteArray()
        
        

        # Preserve phase across calls
        self.phase = 0
        self.freq = 440
        

        self.convert_16_bit = float(2**15)

        coefs = self.getCoef()

        self.white_osc = white_noise.WhiteNoise()
        
        self.white_buffer = self.white_osc.gen_buffer(Meep.SAMPLES_PER_READ) # gen white buffer
        self.filter = sf.FilterChain(coefs)

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
        # pps = self.freq*2*np.pi/format.sampleRate()
        # finalphase = samples*pps + self.phase
        # tone = (
        #   10000 * np.sin(
        #     np.arange(self.phase,
        #               finalphase,
        #               pps)
        #   )
        # ).astype(np.int16)
        
        # self.phase = finalphase % (2*np.pi)
        # return tone.tostring()
        result_buffer = np.zeros(samples)
        self.filter.genBuffer(result_buffer, self.white_osc.gen_buffer(samples))
        result_buffer = result_buffer/np.max(abs(result_buffer))
        result_buffer = np.int16( result_buffer * (self.convert_16_bit-1) )
        return result_buffer.tostring()

    
    
    def readData(self, bytes):

        if bytes > 2 * Meep.SAMPLES_PER_READ:
            bytes = 2 * Meep.SAMPLES_PER_READ
        return self.generateData(self.format,
                                 bytes//2)

    @pyqtSlot(float)
    def changeFreq(self, midi):
        self.freq = math.pow(2,(midi-69)/12)*440
        self.filter.setCoef(self.getCoef())

    def getCoef(self):
        wp = [self.freq*2/SAMPLE_RATE, (self.freq+1)*2/SAMPLE_RATE ]    # multiply by two for nyquist frequency
        ws = [(self.freq-50)*2/SAMPLE_RATE, (self.freq-50)*2/SAMPLE_RATE ]
        self.gpass = 10
        self.gstop = 100
        coefs = scipy.signal.iirdesign(wp,ws,self.gpass,self.gstop,output='sos', ftype='ellip')
        return coefs

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

        
                # Create the port reader object
        self.midiListener = MidiPortReader()

        # Create a thread which will read it
        self.listenerThread = QThread()

        # Take the object and move it
        # to the new thread (it isn't running yet)
        self.midiListener.moveToThread(
            self.listenerThread
        )

        self.midiListener.newNoteFrequency.connect(
            self.generator.changeFreq
        )

        # Tell Qt the function to call
        # when it starts the thread 
        self.listenerThread.started.connect(
            self.midiListener.listener
        )

        # Fingers in ears, eyes tight shut...
        self.listenerThread.start()



if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = ExecutiveToy() #ToneGenerator()
    window.show()
    sys.exit(app.exec_())