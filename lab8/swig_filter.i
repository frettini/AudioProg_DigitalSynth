/* File: swig_filter.i */

/* Name our python module */
%module swig_filter

/* We'll be using C++ standard library strings */
%include <std_string.i>
%include <numpy.i>

/* Put the literal code needed at the top of the output file */
%{
#define SWIG_FILE_WITH_INIT
#include "swig_filter.h"
%}

/* Parse the c++ header file and generate the output file */
%include "swig_filter.h"

%init %{
import_array();
%}

%apply (double* IN_ARRAY1, int DIM1) {
  (const double* in, std::size_t in_size)
};
%apply (double* INPLACE_ARRAY1, int DIM1) {
  (double* out, std::size_t out_size)
};
       