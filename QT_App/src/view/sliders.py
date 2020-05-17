from PyQt5.QtCore import \
    Qt, pyqtSlot, pyqtSignal, QObject
from PyQt5.QtWidgets import \
    QWidget, \
    QSlider, QPushButton, QLabel, \
    QVBoxLayout, QHBoxLayout, QGroupBox

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
        self.activeGen = activeGen     
        # self.createUI(parent)

    def createUI(self, parent):
        groupBox = QGroupBox("Envelope") 

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

        # make sure range slider cannot be equal to 0
        self.ASlid.setRange(1,100)
        self.DSlid.setRange(1,100)
        self.SSlid.setRange(1,100)
        self.RSlid.setRange(1,100)

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

        # ADSRLayout.addWidget(self.envelope)
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
        # range from 0 to 2
        print("A value changed to {}".format(self.ASlid.value()))
        self.sendADSR
        
    @pyqtSlot()
    def DReleased(self):
        # range from 0 to 2
        print("D value changed to {}".format(self.DSlid.value()))
        self.sendADSR

    @pyqtSlot()
    def SReleased(self):
        # range from 0 to 1
        print("S value changed to {}".format(self.SSlid.value()))
        self.sendADSR


    @pyqtSlot()
    def RReleased(self):
        # range from 0 ro 5 s
        print("R value changed to {}".format(self.RSlid.value()))
        self.sendADSR

    def sendADSR(self):
        self.activeGen.adsr.setADSR(
            A = self.ASlid.value()/50,
            D = self.DSlid.value()/50,
            S = self.SSlid.value()/100,
            R = self.RSlid.value()/20
        )



class FiltSlider(QWidget):

    def __init__(self, activeGen, parent=None,):
        QWidget.__init__(self,parent) 
        self.activeGen = activeGen
    
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
        self.activeGen.fNoise.setBW(self.filterSlid.value())


# Deals with Master slider view and sliders signals
class MasterSlider(QWidget):

    def __init__(self, activeGen, parent=None):
        QWidget.__init__(self,parent) 
        self.activeGen = activeGen
    
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
        print("Master value changed to {}".format(self.masterSlid.value()/100))
        self.activeGen.master.setGain(self.masterSlid.value()/100)


# Active generator slider class
class GenSlider(QWidget):

    def __init__(self, activeGen, parent=None):
        QWidget.__init__(self,parent) 
        self.activeGen = activeGen

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
        self.activeGen.setActive(self.genSlid.value())
        
