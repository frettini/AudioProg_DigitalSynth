# Audio Programming : ENG4028

This repo contains the code for the laboratory of the Audio Programming class of the Electronics with Music course (University of Glasgow). Throughout those labs we create audio programming objects such as oscillators and filters to learn about object oriented and audio programming.

In this course module, different aspects of audio programming were explored: optimized oscillators and filters generation, the use of buffering, object oriented programming, SWIG extensions, Qt GUI, MIDI listener, and multi-threading.

**Digital Synthesizer** 

The final assignment tasked us in bringing all those elements together in a digital synthesizer which can be controlled through a Qt GUI. The application can be found in the **Qt_App** folder!

**Requirements**

* python: 3.7 recommended
* numpy: tested on 1.18
* swig 4.0
* QT 5 with PyQT5
* Physical MIDI Keyboard (virtual not tested)

Tested on : 
Windows 10 Pro (version 1903)
macOS mojave (version 10.14.3)
Ubuntu 

**Build Steps**

open a terminal and access the folder:

```bash
cd tone_generator
```

Download all the needed python packages with:

```bash
pip install -r requirements.txt
```

Then run the setup file:

```bash
python setup.py build_ext --inplace
```

The app can then be run using:

```
python tone.py
```
or:

```
python3 tone.py
```

The following folders contain different intermediate tasks and labs that were carried out throughout the year.

**More**

**labs** fodler: 

Contains basic Python and Audio Programming exercise and modules:
 * Read and Write wavfiles module
 * Sine/Triangle/Square oscillator class
 * Recursive oscillator
 * 2nd order IIR filter and concatenated Filters
 
**swig_filter** folder: 

Contains the SWIG extension. The filter code written in Python (in **labs/**) is rewritten in C++. SWIG is used to generate a wrapper and python module. This makes the C++ extension accessible from Python, and greatly optimizes the application.

**Qt_test** folder: 

Contains the Qt and multi-threading extension. A Qt GUI is added using PyQt as well as a MIDI listener and an audio player (Meep) which plays the filter tones. The frequency of the tone is defined by the MIDI notes. Multi-threading is used to make all those parts work together.



