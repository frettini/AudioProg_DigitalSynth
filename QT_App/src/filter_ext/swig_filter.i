/* File: swig_filter.i */

/* Name our python module */
%module swig_filter

/* Put the literal code needed at the top of the output file */
%{
#define SWIG_FILE_WITH_INIT
#include "swig_filter.h"
%}

/* The typemaps interface file lets us use the *OUTPUT Typemap.
   This will enable us to use pointers to variables as return results.
   If more than one *OUTPUT is matched, a tuple gets constructed. */
%include <typemaps.i>

/* Use the numpy interface for ndarrays. See the warning below */
%include <numpy.i>

%init %{
import_array();
%}

/* Match the arguments of our various C++ methods */
%apply (double* IN_ARRAY1, int DIM1) { (const double* in, std::size_t in_size) };
 
%apply (double* INPLACE_ARRAY1, int DIM1) { (double* out, std::size_t out_size) };

%apply (double* IN_ARRAY2, int DIM1, int DIM2) {(const double* in, std::size_t in_size1, std::size_t in_size2)}
/* Parse the c++ header file and generate the output file */
%include "swig_filter.h"
