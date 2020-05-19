import sys
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtWidgets import \
    QApplication, QWidget, QLabel, \
    QVBoxLayout, QHBoxLayout
from PyQt5.QtMultimedia import QAudioFormat, QAudioOutput

from src.view import sliders
from src.pylib.active_gen import ActiveGen
from src.pylib.midi import MidiPortReader
from src.pylib.meep import Meep

# define global variable for the audio format
SAMPLE_RATE = 44100
AUDIO_CHANS = 1
SAMPLE_SIZE = 16
CTRL_INTERVAL = 100 # milliseconds of audio


class ToneWindow(QWidget):
    """
    Central Widget of the application.
    
    Defines the format of the audio channel and initializes the midi listener, 
    generators and modifiers. The midi listener is operated on separate thread 
    handled by a Qthread. The view components are initialized and put together 
    in a general layout using the CreateUI method.
    """

    def __init__(self, parent=None):
        print("Tone Widget inst")
        QWidget.__init__(self, parent)


        self.activeGen = ActiveGen(sampleRate=SAMPLE_RATE, samplePerRead=Meep.SAMPLES_PER_READ)
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
        
        # initialize and start the audio playback
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

        # Connect the signals to slot functions
        self.midiListener.newNoteFrequency.connect(
            self.activeGen.setFreq
        )
        self.midiListener.newNotePress.connect(
            self.activeGen.adsr.setNote
        )

        # Tell Qt the function to call
        # when it starts the thread 
        self.listenerThread.started.connect(
            self.midiListener.listener
        )
        # start the thread
        self.listenerThread.start()



    def createUI(self, parent):

        """Receives a parent QWidget and produces the view in it"""

        print("Create UI")
        slidLayout = QHBoxLayout()
        vLayout = QVBoxLayout(self)
        vLayout.setSpacing(10)

        # initialize title label and UI constraints
        self.title = QLabel(self)
        self.title.setText("Tone Generator")
        self.title.setMargin(10)
        self.title.setFixedHeight(50)
        self.title.setFixedWidth(400)
        self.title.setAlignment(Qt.AlignCenter)

        # set title style
        self.title.setStyleSheet("""
                font-family : "Lucida Console";
                font-size: 20px;
                color : #F2F2F2;
                border: 2px solid green;
                border-radius: 4px;
                border-color: #082126;
                padding: 2px;
                background-color : #0E3740 ;
        """)
        # set background color
        self.setStyleSheet(
            " background-color : #082126 ; "
        )

        # initialize the view components
        filtSlider = sliders.FiltSlider(self.activeGen, self).createUI(parent)
        adsrSlider = sliders.ADSRSlider(self.activeGen, self).createUI(parent)
        masterSlider = sliders.MasterSlider(self.activeGen, self).createUI(parent)
        genSlider = sliders.GenSlider(self.activeGen, self).createUI(parent)

        # add the two sliders and ADSR layout in a horizontal layout
        slidLayout.addStretch(1)
        slidLayout.addWidget(filtSlider)
        slidLayout.addStretch(1)
        slidLayout.addWidget(adsrSlider, Qt.AlignHCenter)    
        slidLayout.addStretch(1)    
        slidLayout.addWidget(masterSlider)
        slidLayout.addStretch(1)

        # put all components in the vertical layout    
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
