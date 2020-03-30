#!/usr/bin/env python

"""
setup.py file for SWIG example
"""

from distutils.core import setup, Extension
import numpy

swig_filter_module = Extension('_swig_filter',
                           sources=['swig_filter_wrap.cxx', 'swig_filter.cxx'],
                           )

setup (name = 'swig_filter',
       version = '0.1',
       author      = "SWIG Docs",
       description = """swig filter test""",
       ext_modules = [swig_filter_module],
       py_modules = ["swig_filter"],
       include_dirs=[numpy.get_include()]
       )