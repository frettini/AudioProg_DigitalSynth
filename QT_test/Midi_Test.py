import mido
import rtmidi


mido.set_backend('mido.backends.rtmidi')
print("Using MIDI APIs: {}".format(mido.backend.module.get_api_names()))

mido.get_input_names()

with mido.open_input(
    virtual=False
) as mip:
    for mmsg in mip:
        print(mmsg.type)
        print(mmsg.bytes())