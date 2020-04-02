#!/usr/bin/env python

"""
setup.py file for SWIG example
"""

# system import
from distutils.core import setup, Extension
import os

# 3rd party module
import numpy

# Obtain the numpy include directory.  This logic works across numpy versions.
try:
    numpy_include = numpy.get_include()
except AttributeError:
    numpy_include = numpy.get_numpy_include()

# implies that swig_filter_wrap has to be done already
# swig_filter_module = Extension('_swig_filter', 
#                            sources=['swig_filter_wrap.cxx', 'swig_filter.cxx'],
#                            ) 

srcFiles = ['swig_filter.i','swig_filter_wrap.cpp', 'swig_filter.cxx']



swig_filter_module = Extension('_swig_filter', 
                           sources=srcFiles,
                           swig_opts = ['-c++', '-modern']
                           ) 

setup (name = 'swig_filter',
       version = '0.1',
       author      = "Nicolae Marton",
       description = """Modules that implements audio filters in C""",
       ext_modules = [swig_filter_module],
       py_modules = ["swig_filter"],
       include_dirs=[numpy_include] #required if dealing with virtual environments
       )