import os
from PyQt5.QtCore import \
    Qt, pyqtSlot, pyqtSignal, QObject, QFile
from PyQt5.QtWidgets import \
    QWidget, \
    QSlider, QPushButton, QLabel, \
    QVBoxLayout, QHBoxLayout, QGroupBox

class UIHelper:
    """
    Static class which provides helper functions to build the view.
    """

    @staticmethod
    def labSlidLayout(slider, label, labelName):
        """ 
        Returns a layout containing a label with a set name on top of a slider. 
        """
        
        layout = QVBoxLayout()

        # set label name and constraints
        label.setText(labelName)
        label.setMaximumHeight(50)
        label.setAlignment(Qt.AlignCenter)
        label.setMargin(5)
        
        # set slider constraint
        slider.setMinimumHeight(100)

        # add the widgets to the vertical layout
        layout.addWidget(label)
        layout.addWidget(slider)
        layout.setAlignment(slider, Qt.AlignJustify)

        return layout


class ADSRSlider(QWidget):
    """ 
    Defines the view of the ADSR sliders.

    Initializes the widgets, layout and constraints in the createUI method. 
    Each slider has a dedicated receiver slot which is connected to the 
    release slider event. The slot methods call the setADSR method which updates
    the ADSR values.
    """
    def __init__(self, activeGen, parent=None):
        QWidget.__init__(self,parent)   
        self.activeGen = activeGen     
        # self.createUI(parent)

    def createUI(self, parent):
        """ Receives a parent QWidget and produces the ADSR groupBox."""

        # groupbox add a border and the ability to resize the frame
        groupBox = QGroupBox("Envelope") 
        subLayout = QHBoxLayout()
        
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

        # set ticker to an initial value
        self.ASlid.setValue(50)
        self.DSlid.setValue(50)
        self.SSlid.setValue(70)
        self.RSlid.setValue(40)

        # slider titles
        self.ALabel = QLabel(self)
        self.DLabel = QLabel(self)
        self.SLabel = QLabel(self)
        self.RLabel = QLabel(self)

        # add them to a sublayout (to add the section title)
        subLayout.addStretch(1)
        subLayout.addLayout(UIHelper.labSlidLayout(self.ASlid, self.ALabel, "Attack"))
        subLayout.addStretch(1)
        subLayout.addLayout(UIHelper.labSlidLayout(self.DSlid, self.DLabel, "Decay"))
        subLayout.addStretch(1)
        subLayout.addLayout(UIHelper.labSlidLayout(self.SSlid, self.SLabel, "Sustain"))
        subLayout.addStretch(1)
        subLayout.addLayout(UIHelper.labSlidLayout(self.RSlid, self.RLabel, "Release"))
        subLayout.addStretch(1)

        # add margin arround each element
        # Justify the widget to be equally spaced in the layout
        subLayout.setContentsMargins(20,20,20,20)
        subLayout.setAlignment(Qt.AlignJustify)
        
        # connect the release signals to the slots 
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

        # add the final layout to a groupbox
        groupBox.setLayout(subLayout)

        # load and apply the style sheet
        styleSheet = open(os.path.join("src", "view", "style.qss"), "r")
        groupBox.setStyleSheet(styleSheet.read())

        return groupBox

    # 
    @pyqtSlot()
    def AReleased(self):
        # range from 0 to 2
        print("A value changed to {}".format(self.ASlid.value()))
        self.sendADSR()
        
    @pyqtSlot()
    def DReleased(self):
        # range from 0 to 2
        print("D value changed to {}".format(self.DSlid.value()))
        self.sendADSR()

    @pyqtSlot()
    def SReleased(self):
        # range from 0 to 1
        print("S value changed to {}".format(self.SSlid.value()))
        self.sendADSR()


    @pyqtSlot()
    def RReleased(self):
        # range from 0 ro 5 s
        print("R value changed to {}".format(self.RSlid.value()))
        self.sendADSR()

    def sendADSR(self):
        """ Update the adsr modifier with the current values of the sliders. """
        
        self.activeGen.adsr.setADSR(
            A = self.ASlid.value()/50,
            D = self.DSlid.value()/50,
            S = self.SSlid.value()/100,
            R = self.RSlid.value()/20
        )



class FiltSlider(QWidget):
    """ 
    Defines the view of the filter sharpness slider. 

    Initializes the widgets, layout and constraints in the createUI method. 
    The slider release event is connected to a slot method which updates the 
    sharpness of the filtered noise generator.
    """

    def __init__(self, activeGen, parent=None, styleSheet = None):
        QWidget.__init__(self,parent) 
        self.activeGen = activeGen
    

    def createUI(self, parent):
        """ Receives a parent QWidget and returns the Filter Q groupBox."""

        #Box Layout which groups sliders with a title and borders
        filterBox = QGroupBox("Filter Q")
        filterBox.setFixedWidth(85)

        #create sub widget
        self.filterLabel = QLabel(self)

        # initialize the slider, its range and value
        self.filterSlid = QSlider(Qt.Vertical)
        self.filterSlid.setRange(1,100)
        self.filterSlid.setValue(100)

        # connect the release signal to the update function
        self.filterSlid.sliderReleased.connect(
            self.filterReleased
        )

        # add a label to the slider
        subLayout = UIHelper.labSlidLayout(self.filterSlid, self.filterLabel, "Q")
        subLayout.setContentsMargins(20,20,20,20)

        #create layout with label on top of slider
        filterBox.setLayout(subLayout)

        # load and apply the style sheet
        styleSheet = open(os.path.join("src", "view", "style.qss"), "r")
        filterBox.setStyleSheet(styleSheet.read())
        
        return filterBox

    @pyqtSlot()
    def filterReleased(self):
        """ Update the filter generator with a modified value of the slider. """


        print("Filter value changed to {}".format(self.filterSlid.value()))
        self.activeGen.fNoise.setQ(self.filterSlid.value()*-1 + 100)


# Deals with Master slider view and sliders signals
class MasterSlider(QWidget):
    """ 
    Defines the view of the master gain slider. 

    Initializes the widgets, layout and constraints in the createUI method. 
    The slider release event is connected to a slot method which updates the 
    overall master gain.
    """

    def __init__(self, activeGen, parent=None):
        QWidget.__init__(self,parent) 
        self.activeGen = activeGen
        
    
    def createUI(self, parent):
        """ Receives a parent QWidget and produces the master groupBox"""

        masterBox = QGroupBox("Master")
        masterBox.setMinimumWidth(85)

        self.masterLabel = QLabel(self)
        
        # initialize the slider, its range and value
        self.masterSlid = QSlider(Qt.Vertical)
        self.masterSlid.setRange(0,100)
        self.masterSlid.setValue(70)

        # connect the release signal to the update function
        self.masterSlid.sliderReleased.connect(
            self.masterReleased
        )

        # add a label to the slider
        masterLayout = UIHelper.labSlidLayout(self.masterSlid, self.masterLabel, "Gain")
        masterLayout.setContentsMargins(20,20,20,20)

        masterBox.setLayout(masterLayout)

        # load and apply the style sheet
        styleSheet = open(os.path.join("src", "view", "style.qss"), "r")
        masterBox.setStyleSheet(styleSheet.read())

        return masterBox

    @pyqtSlot()
    def masterReleased(self):
        """ Update the master gain with a modified value of the slider. """

        print("Master value changed to {}".format(self.masterSlid.value()/100))
        self.activeGen.master.setGain(self.masterSlid.value()/100)


class GenSlider(QWidget):
    """ 
    Defines the view of the Active Generator Selector. 

    Initializes the widgets, layout and constraints in the createUI method. 
    The slider release event is connected to a slot method which updates the 
    the active generator.
    """

    def __init__(self, activeGen, parent=None):
        QWidget.__init__(self,parent) 
        self.activeGen = activeGen

    def createUI(self, parent):
        """ Receives a parent QWidget and produces the active generator groupBox."""

        # create active generator slider
        # set range from 0 to 2 and add ticks
        # the slider will be used as a switch between generators
        max = 2
        self.genSlid = QSlider(Qt.Horizontal)
        self.genSlid.setRange(0,max)
        self.genSlid.setTickPosition(QSlider.TicksBelow)
        self.genSlid.setMinimumWidth(400)
        self.genSlid.setMaximumWidth(800)
        

        # define generator labels
        # iterate through the list and add a label per generator
        labels = ["Filter", "Sine", "Noise"]
        labelLayout = QHBoxLayout()

        ind = 0
        for lab in labels:
            label = QLabel(lab)
            labelLayout.addWidget(label)
            if ind < max:
                labelLayout.addStretch()
                ind += 1

        # align to the ticks
        labelLayout.setAlignment(Qt.AlignJustify)
        labelLayout.setAlignment(Qt.AlignTop)

        subLayout = QVBoxLayout()

        # add sliders and labels to a layout
        subLayout.addWidget(self.genSlid)
        subLayout.addLayout(labelLayout)
        subLayout.setAlignment(self.genSlid, Qt.AlignCenter)
        subLayout.setAlignment(self.genSlid, Qt.AlignJustify)

        # connect the release signal to the update function
        self.genSlid.sliderReleased.connect(
            self.genReleased
        )

        # add title and constraints
        genGroup = QGroupBox("Active Generator")
        genGroup.setAlignment(Qt.AlignCenter)
        genGroup.setMaximumHeight(200)
        genGroup.setLayout(subLayout)

        # load and apply the style sheet
        styleSheet = open(os.path.join("src", "view", "style.qss"), "r")
        genGroup.setStyleSheet(styleSheet.read())
        
        return genGroup


    @pyqtSlot()
    def genReleased(self):
        """ Update the active generator with a modified value of the slider."""

        print("Gen value changed to {}".format(self.genSlid.value()))
        self.activeGen.setActive(self.genSlid.value())
        
