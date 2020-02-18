/* File: simple_hello.i */

/* Name our python module */
%module simple_hello

/* We'll be using C++ standard library strings */
%include <std_string.i>

/* Put the literal code needed at the top of the output file */
%{
#define SWIG_FILE_WITH_INIT
#include "simple_hello.h"
%}

/* Parse the c++ header file and generate the output file */
%include "simple_hello.h"