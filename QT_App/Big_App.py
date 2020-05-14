import sys
from PyQt5.QtCore import \
    Qt, pyqtSlot, pyqtSignal, QObject, QThread, QByteArray, QIODevice
from PyQt5.QtWidgets import \
    QApplication, QWidget, \
    QSlider, QPushButton, QLabel, \
    QMessageBox, \
    QVBoxLayout, QHBoxLayout, QGroupBox
from PyQt5.QtMultimedia import QAudioFormat, QAudioOutput

from src.view import sliders
# import math
# import numpy as np
# import mido
# import rtmidi
# import scipy.signal

# from swig_module import swig_filter as sf
# from swig_module.modules import noise

SAMPLE_RATE = 44100
AUDIO_CHANS = 1
SAMPLE_SIZE = 16
CTRL_INTERVAL = 100 # milliseconds of audio

class UIHelper:

    # test static methods
    # this could have also been done extending the QSlider widget
    @staticmethod
    def labSlidLayout(slider, label, labelName):
        layout = QVBoxLayout()
        label.setText(labelName)
        
        # label.setAlignment(Qt.AlignCenter)

        layout.addWidget(label)
        layout.addWidget(slider)

        return layout


class ADSRSlider(QWidget):

    def __init__(self, activeGen, parent=None):
        QWidget.__init__(self,parent)        
        # self.createUI(parent)

    def createUI(self, parent):
        groupBox = QGroupBox() 

        ADSRLayout = QVBoxLayout()
        
        subLayout = QHBoxLayout()
        
        ALayout = QVBoxLayout()
        DLayout = QVBoxLayout()
        SLayout = QVBoxLayout()
        RLayout = QVBoxLayout()
        

        # create the middle sliders for ADSR
        self.ASlid = QSlider(Qt.Vertical)
        self.DSlid = QSlider(Qt.Vertical)
        self.SSlid = QSlider(Qt.Vertical)
        self.RSlid = QSlider(Qt.Vertical)

        # add a section title
        self.envelope = QLabel(self)
        self.envelope.setText("Envelope")

        # slider titles
        self.ALabel = QLabel(self)
        self.DLabel = QLabel(self)
        self.SLabel = QLabel(self)
        self.RLabel = QLabel(self)

        # add them to a sublayout (to add the section title)
        subLayout.addLayout(UIHelper.labSlidLayout(self.ASlid, self.ALabel, "Attack"))
        subLayout.addLayout(UIHelper.labSlidLayout(self.DSlid, self.DLabel, "Decay"))
        subLayout.addLayout(UIHelper.labSlidLayout(self.SSlid, self.SLabel, "Sustain"))
        subLayout.addLayout(UIHelper.labSlidLayout(self.RSlid, self.RLabel, "Release"))

        ADSRLayout.addWidget(self.envelope)
        ADSRLayout.addLayout(subLayout)
        

        self.ASlid.sliderReleased.connect(
            self.AReleased
        )
        self.DSlid.sliderReleased.connect(
            self.DReleased
        )
        self.SSlid.sliderReleased.connect(
            self.SReleased
        )
        self.RSlid.sliderReleased.connect(
            self.RReleased
        )

        groupBox.setLayout(ADSRLayout)

        return groupBox




    @pyqtSlot()
    def AReleased(self):
        print("A value changed to {}".format(self.ASlid.value()))
        
    @pyqtSlot()
    def DReleased(self):
        print("D value changed to {}".format(self.DSlid.value()))

    @pyqtSlot()
    def SReleased(self):
        print("S value changed to {}".format(self.SSlid.value()))

    @pyqtSlot()
    def RReleased(self):
        print("R value changed to {}".format(self.RSlid.value()))



class FiltSlider(QWidget):

    def __init__(self, activeGen, parent=None,):
        QWidget.__init__(self,parent) 
    
    def createUI(self, parent):
        #Box Layout which groups sliders with a title and borders
        filterBox = QGroupBox("Filtered Noise")

        #create sub widget
        self.filterLabel = QLabel(self)
        self.filterSlid = QSlider(Qt.Vertical)

        self.filterSlid.sliderReleased.connect(
            self.filterReleased
        )

        #create lyaout with label on top of slider
        filterBox.setLayout(UIHelper.labSlidLayout(self.filterSlid, self.filterLabel, "Q"))
        return filterBox

    @pyqtSlot()
    def filterReleased(self):
        print("Filter value changed to {}".format(self.filterSlid.value()))


# Deals with Master slider view and sliders signals
class MasterSlider(QWidget):

    def __init__(self, activeGen, parent=None):
        QWidget.__init__(self,parent) 
    
    def createUI(self, parent):
        filterBox = QGroupBox("Master")

        self.masterLabel = QLabel(self)
        self.masterSlid = QSlider(Qt.Vertical)

        self.masterSlid.sliderReleased.connect(
            self.masterReleased
        )

        filterBox.setLayout(UIHelper.labSlidLayout(self.masterSlid, self.masterLabel, "Gain") )
        return filterBox

    @pyqtSlot()
    def masterReleased(self):
        print("Master value changed to {}".format(self.masterSlid.value()))


# Active generator slider class
class GenSlider(QWidget):

    def __init__(self, activeGen, parent=None):
        QWidget.__init__(self,parent) 

    def createUI(self, parent):

        genLayout = QVBoxLayout()
        self.genLabel = QLabel(self)

        max = 2
        # create active generator slider
        # change range from 0 to 2 and add ticks
        self.genSlid = QSlider(Qt.Horizontal)
        self.genSlid.setRange(0,max)
        self.genSlid.setTickPosition(QSlider.TicksBelow)
        
        labels = ["Flute", "Sine", "Noise"]
        
        labelLayout = QHBoxLayout()

        ind = 0
        for lab in labels:
            label = QLabel(lab)
            labelLayout.addWidget(label)
            if ind < max:
                labelLayout.addStretch()
                ind += 1

        labelLayout.setAlignment(Qt.AlignJustify)

        genLayout.addLayout(UIHelper.labSlidLayout(self.genSlid, self.genLabel, "Active Generator"))
        genLayout.addLayout(labelLayout)

        self.genSlid.sliderReleased.connect(
            self.genReleased
        )

        return genLayout


    @pyqtSlot()
    def genReleased(self):
        print("Gen value changed to {}".format(self.genSlid.value()))
        

class ToneWidget(QWidget):

    def __init__(self, parent=None):
        print("Tone Widget inst")
        QWidget.__init__(self, parent)
        self.createUI(parent)

    def createUI(self, parent):
        print("Create UI")
        slidLayout = QHBoxLayout()
        vLayout = QVBoxLayout(self)

        #create dummy active gen for now
        activeGen = None

        #create the two other sliders
        self.MasterSlid = QSlider(Qt.Vertical)
        self.QSlid = QSlider(Qt.Vertical)
        
        # add the two sliders and ADSR layout in a horizontal layout
        slidLayout.addStretch(1)
        slidLayout.addWidget(sliders.FiltSlider(activeGen, self).createUI(parent))
        slidLayout.addStretch(1)
        slidLayout.addWidget(sliders.ADSRSlider(activeGen, self).createUI(parent))    
        slidLayout.addStretch(1)    
        slidLayout.addWidget(sliders.MasterSlider(activeGen, self).createUI(parent))
        slidLayout.addStretch(1)    


        self.title = QLabel(self)
        self.title.setText("Big App")

        vLayout.addWidget(self.title)
        vLayout.addLayout(slidLayout)
        vLayout.addLayout(sliders.GenSlider(activeGen, self).createUI(parent))

        


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = ToneWidget()
    window.show()
    sys.exit(app.exec_())
