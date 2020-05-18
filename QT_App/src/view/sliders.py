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
        label.setMaximumHeight(50)
        label.setAlignment(Qt.AlignCenter)
        # label.setStyleSheet("QLabel { background-color : red; color : blue; }")
        label.setMargin(5)
        # slider.setMaximumWidth()
        
        slider.setMinimumHeight(100)

        layout.addWidget(label)
        layout.addWidget(slider)
        # layout.setAlignment(slider, Qt.AlignCenter)
        layout.setAlignment(slider, Qt.AlignJustify)


        return layout


class ADSRSlider(QWidget):

    def __init__(self, activeGen, parent=None):
        QWidget.__init__(self,parent)   
        self.activeGen = activeGen     
        # self.createUI(parent)

    def createUI(self, parent):
        groupBox = QGroupBox("Envelope") 

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


        subLayout.setContentsMargins(20,20,20,20)
        subLayout.setAlignment(Qt.AlignJustify)
        

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

        groupBox.setLayout(subLayout)
        groupBox.setStyleSheet(
            """
           QGroupBox, QLabel {
               font-family : "Lucida Console";
               background-color :  #0E3740;
               border : #082126;
               color : #F2F2F2;
           }

           QGroupBox {
               font-weight: bold;
               font-size: 13px;
               padding: 10px;
           }

           QSlider{
               background-color : #0E3740; 
           }

           QSlider::groove:vertical {
                background: #082126;
                border: 1px solid;
                margin: 0px;
            }

            QSlider::handle:vertical {
                background-color: #077373;
                border: 1px solid;
                height: 10px;
                margin: 0 -4px;
            }

            QSlider::add-page:vertical{
                background: #04BFBF;
            }

            QSlider::sub-page:vertical{
                background: #082126;
            }

            QSlider::groove:horizontal {
                background: #082126;
                border: 1px solid;
                margin: 0px;
            }

            QSlider::handle:horizontal {
                background-color: #077373;
                border: 1px solid;
                height: 10px;
                margin: 0 -4px;
            }

            QSlider::add-page:horizontal{
                background: #04BFBF;
            }

            QSlider::sub-page:horizontal{
                background: #082126;
            }
           """
        )

        return groupBox

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

    # update all the adsr values
    def sendADSR(self):
        self.activeGen.adsr.setADSR(
            A = self.ASlid.value()/50,
            D = self.DSlid.value()/50,
            S = self.SSlid.value()/100,
            R = self.RSlid.value()/20
        )



class FiltSlider(QWidget):

    def __init__(self, activeGen, parent=None, styleSheet = None):
        QWidget.__init__(self,parent) 
        self.activeGen = activeGen
    

    def createUI(self, parent):
        #Box Layout which groups sliders with a title and borders
        filterBox = QGroupBox("Filter Q")
        filterBox.setFixedWidth(85)

        #create sub widget
        self.filterLabel = QLabel(self)

        # initialize the slider, its range and value
        self.filterSlid = QSlider(Qt.Vertical)
        self.filterSlid.setRange(1,100)
        self.filterSlid.setValue(100)


        self.filterSlid.sliderReleased.connect(
            self.filterReleased
        )

        subLayout = UIHelper.labSlidLayout(self.filterSlid, self.filterLabel, "Q")
        subLayout.setContentsMargins(20,20,20,20)

        #create layout with label on top of slider
        filterBox.setLayout(subLayout)

        filterBox.setStyleSheet(
            """
           QGroupBox, QLabel {
               font-family : "Lucida Console";
               background-color :  #0E3740;
               border : #082126;
               color : #F2F2F2;
           }

           QGroupBox {
               font-weight: bold;
               font-size: 13px;
               padding: 10px;
           }

           QSlider{
               background-color : #0E3740; 
           }

           QSlider::groove:vertical {
                background: #082126;
                border: 1px solid;
                margin: 0px;
            }

            QSlider::handle:vertical {
                background-color: #077373;
                border: 1px solid;
                height: 10px;
                margin: 0 -4px;
            }

            QSlider::add-page:vertical{
                background: #04BFBF;
            }

            QSlider::sub-page:vertical{
                background: #082126;
            }

            QSlider::groove:horizontal {
                background: #082126;
                border: 1px solid;
                margin: 0px;
            }

            QSlider::handle:horizontal {
                background-color: #077373;
                border: 1px solid;
                height: 10px;
                margin: 0 -4px;
            }

            QSlider::add-page:horizontal{
                background: #04BFBF;
            }

            QSlider::sub-page:horizontal{
                background: #082126;
            }
           """
           
        )
        
        return filterBox

    @pyqtSlot()
    def filterReleased(self):
        print("Filter value changed to {}".format(self.filterSlid.value()))
        self.activeGen.fNoise.setQ(self.filterSlid.value()*-1 + 100)


# Deals with Master slider view and sliders signals
class MasterSlider(QWidget):

    def __init__(self, activeGen, parent=None):
        QWidget.__init__(self,parent) 
        self.activeGen = activeGen
    
    def createUI(self, parent):
        masterBox = QGroupBox("Master")
        masterBox.setMinimumWidth(85)

        self.masterLabel = QLabel(self)
        
        # initialize the slider, its range and value
        self.masterSlid = QSlider(Qt.Vertical)
        self.masterSlid.setRange(0,100)
        self.masterSlid.setValue(70)

        self.masterSlid.sliderReleased.connect(
            self.masterReleased
        )

        masterLayout = UIHelper.labSlidLayout(self.masterSlid, self.masterLabel, "Gain")
        masterLayout.setContentsMargins(20,20,20,20)

        masterBox.setLayout(masterLayout)

        masterBox.setStyleSheet(
            """
           QGroupBox, QLabel {
               font-family : "Lucida Console";
               background-color :  #0E3740;
               border : #082126;
               color : #F2F2F2;
           }

           QGroupBox {
               font-weight: bold;
               font-size: 13px;
               padding: 10px;
           }

           QSlider{
               background-color : #0E3740; 
           }

           QSlider::groove:vertical {
                background: #082126;
                border: 1px solid;
                margin: 0px;
            }

            QSlider::handle:vertical {
                background-color: #077373;
                border: 1px solid;
                height: 10px;
                margin: 0 -4px;
            }

            QSlider::add-page:vertical{
                background: #04BFBF;
            }

            QSlider::sub-page:vertical{
                background: #082126;
            }

            QSlider::groove:horizontal {
                background: #082126;
                border: 1px solid;
                margin: 0px;
            }

            QSlider::handle:horizontal {
                background-color: #077373;
                border: 1px solid;
                height: 10px;
                margin: 0 -4px;
            }

            QSlider::add-page:horizontal{
                background: #04BFBF;
            }

            QSlider::sub-page:horizontal{
                background: #082126;
            }
           """
        )

        return masterBox

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

        # create active generator slider
        # change range from 0 to 2 and add ticks
        max = 2
        self.genSlid = QSlider(Qt.Horizontal)
        self.genSlid.setRange(0,max)
        self.genSlid.setTickPosition(QSlider.TicksBelow)
        self.genSlid.setMinimumWidth(400)
        self.genSlid.setMaximumWidth(800)
        

        # create labels and add them to a sub layout
        labels = ["Filter", "Sine", "Noise"]
        labelLayout = QHBoxLayout()

        ind = 0
        for lab in labels:
            label = QLabel(lab)
            labelLayout.addWidget(label)
            if ind < max:
                labelLayout.addStretch()
                ind += 1

        #align to the ticks
        labelLayout.setAlignment(Qt.AlignJustify)
        labelLayout.setAlignment(Qt.AlignTop)

        # genWidget = QWidget()
        subLayout = QVBoxLayout()

        # subLayout.addWidget(self.genLabel)
        subLayout.addWidget(self.genSlid)
        subLayout.addLayout(labelLayout)
        subLayout.setAlignment(self.genSlid, Qt.AlignCenter)
        subLayout.setAlignment(self.genSlid, Qt.AlignJustify)

        # genLayout.addLayout(subLayout)
        # genLayout.addLayout(labelLayout)

        self.genSlid.sliderReleased.connect(
            self.genReleased
        )

        genGroup = QGroupBox("Active Generator")
        genGroup.setAlignment(Qt.AlignCenter)

        genGroup.setMaximumHeight(200)
        genGroup.setLayout(subLayout)
        genGroup.setStyleSheet(
            """
           QGroupBox, QLabel {
               font-family : "Lucida Console";
               background-color :  #0E3740;
               border : #082126;
               color : #F2F2F2;
           }

           QGroupBox {
               font-weight: bold;
               font-size: 13px;
               padding: 10px;
           }

           QSlider{
               background-color : #0E3740; 
           }


            QSlider::groove:horizontal {
                background: #082126;
                height: 8px;
                border: 1px solid;
                margin: 0px;
            }

            QSlider::handle:horizontal {
                background-color: #077373;
                border: 1px solid;
                width: 10px;
                margin: -4px 0;
            }

            QSlider::add-page:horizontal{
                background: #082126;
            }

            QSlider::sub-page:horizontal{
                background: #082126 ;
            }
           """
        )
        
        return genGroup


    @pyqtSlot()
    def genReleased(self):
        print("Gen value changed to {}".format(self.genSlid.value()))
        self.activeGen.setActive(self.genSlid.value())
        
