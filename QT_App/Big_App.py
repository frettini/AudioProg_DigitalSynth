import sys
from PyQt5.QtCore import \
    Qt, pyqtSlot, pyqtSignal, QObject, QThread, QByteArray, QIODevice
from PyQt5.QtWidgets import \
    QApplication, QWidget, \
    QSlider, QPushButton, QLabel, \
    QMessageBox, \
    QVBoxLayout, QHBoxLayout, QGroupBox
from PyQt5.QtMultimedia import QAudioFormat, QAudioOutput

import numpy as np
import math
import mido
import rtmidi

from src.view import sliders
from src.pylib.active_gen import ActiveGen
# import scipy.signal

# from swig_module import swig_filter as sf
# from swig_module.modules import noise

SAMPLE_RATE = 44100
AUDIO_CHANS = 1
SAMPLE_SIZE = 16
CTRL_INTERVAL = 100 # milliseconds of audio


class MidiPortReader(QObject):

    # Create a signal for when a
    # MIDI note_on happens
    newNoteFrequency = pyqtSignal(float)
    newNotePress = pyqtSignal(bool)
    
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
                # print(mmsg.type)
                # print(mmsg.bytes())
                
                # convert midi to frequency
                freq = math.pow(2,(float(mmsg.bytes()[1])-69)/12)*440

                # Only communicate via the Qt signal
                # Qt will stop us hurting ourselves
                
                self.newNoteFrequency.emit(float(freq))
                
                if mmsg.type == "note_on":
                    status = True
                if mmsg.type == "note_off":
                    status = False
                    
                self.newNotePress.emit(status)


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




class ToneWindow(QWidget):

    def __init__(self, parent=None):
        print("Tone Widget inst")
        QWidget.__init__(self, parent)


        self.activeGen = ActiveGen()
        self.createUI(parent)

        # Meep playback format initialization
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

        # Audio Output init
        self.output = QAudioOutput(format, self)
        output_buffer_size = \
            int(2*SAMPLE_RATE \
                 *CTRL_INTERVAL/1000)
        self.output.setBufferSize(
            output_buffer_size
        )
        
        self.generator = Meep(format, self.activeGen, self )        
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
            self.activeGen.setFreq
        )

        self.midiListener.newNotePress.connect(self.activeGen.adsr.setNote)

        # Tell Qt the function to call
        # when it starts the thread 
        self.listenerThread.started.connect(
            self.midiListener.listener
        )

        # Fingers in ears, eyes tight shut...
        self.listenerThread.start()




    def createUI(self, parent):
        print("Create UI")
        slidLayout = QHBoxLayout()
        vLayout = QVBoxLayout(self)
        vLayout.setSpacing(10)

        #create the two other sliders
        self.MasterSlid = QSlider(Qt.Vertical)
        self.QSlid = QSlider(Qt.Vertical)
        
        # add the two sliders and ADSR layout in a horizontal layout
        slidLayout.addStretch(1)
        slidLayout.addWidget(sliders.FiltSlider(self.activeGen, self).createUI(parent))
        slidLayout.addStretch(1)
        slidLayout.addWidget(sliders.ADSRSlider(self.activeGen, self).createUI(parent), Qt.AlignHCenter)    
        slidLayout.addStretch(1)    
        slidLayout.addWidget(sliders.MasterSlider(self.activeGen, self).createUI(parent))
        slidLayout.addStretch(1)


        self.title = QLabel(self)
        self.title.setText("The Tone Generator")
        self.title.setMargin(10)
        self.title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                border: 2px solid green;
                border-radius: 4px;
                padding: 2px;
                background-color : yellow ;
            }  
        """)
        
        self.title.setFixedHeight(50)
        self.title.setFixedWidth(400)
        self.title.setAlignment(Qt.AlignCenter)

    
        genSlider = sliders.GenSlider(self.activeGen, self).createUI(parent)
        
        vLayout.addWidget(self.title)
        vLayout.setAlignment(self.title,Qt.AlignCenter)
        vLayout.addSpacing(20)
        vLayout.addLayout(slidLayout)
        vLayout.addSpacing(20)

        vLayout.addWidget(genSlider)
        vLayout.setAlignment(genSlider,Qt.AlignCenter)

        


if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = ToneWindow()
    window.setWindowTitle("Tone Generator")
    window.show()
    sys.exit(app.exec_())
