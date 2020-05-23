import math
import mido
# import rtmidi
from PyQt5.QtCore import QObject, pyqtSignal


class MidiPortReader(QObject):
    """ 
    MIDI listener Class.

    This QObject establishes port connection with a MIDI device.
    The listener methods waits and reads MIDI inputs. It uses 
    pyqt signals to emit the information.
    """

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
        """ Listen to the MIDI input and emit data using pyqt signals."""

        with mido.open_input(virtual=False) as mip:
            for mmsg in mip:
                
                # convert midi to frequency
                freq = math.pow(2,(float(mmsg.bytes()[1])-69)/12)*440

                # detect onsets and offsets
                if mmsg.type == "note_on":
                    status = True
                    # change frequency only on onsets
                    self.newNoteFrequency.emit(float(freq))
                if mmsg.type == "note_off":
                    status = False
                    
                # emit status
                self.newNotePress.emit(status)
