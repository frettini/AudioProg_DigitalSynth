#!/usr/bin/env python

"""
setup.py file for SWIG example
"""

from distutils.core import setup, Extension
import numpy

# implies that swig_filter_wrap has to be done already
# swig_filter_module = Extension('_swig_filter', 
#                            sources=['swig_filter_wrap.cxx', 'swig_filter.cxx'],
#                            ) 

swig_filter_module = Extension('_swig_filter', 
                           sources=['swig_filter.i','swig_filter_wrap.cpp', 'swig_filter.cxx'],
                           swig_opts = ['-c++']
                           ) 

setup (name = 'swig_filter',
       version = '0.1',
       author      = "Nicolae Marton",
       description = """Modules that implements audio filters in C""",
       ext_modules = [swig_filter_module],
       py_modules = ["swig_filter"],
       include_dirs=[numpy.get_include()] #required if dealing with virtual environments
       )