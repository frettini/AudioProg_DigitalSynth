# Audio Programming : ENG4028

This repo contains the code for the laboratory of the Audio Programming class of the Electronics with Music course (University of Glasgow). Throughout those labs we create audio programming objects such as oscillators and filters to learn about object oriented and audio programming.

In this course module, different aspects of audio programming were explored: optimized oscillators and filters generation, the use of buffering, object oriented programming, SWIG extensions, Qt GUI, MIDI listener, and multi-threading. The following list directs to those different sections.

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
