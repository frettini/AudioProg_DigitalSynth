#!/usr/bin/env python

"""
setup.py file for SWIG example
"""

from distutils.core import setup, Extension


min_max_sum_module = Extension('_min_max_sum',
                           sources=['min_max_sum_wrap.cxx', 'min_max_sum.cxx'],
                           )

setup (name = 'min_max_sum',
       version = '0.1',
       author      = "SWIG Docs",
       description = """min max sum test""",
       ext_modules = [min_max_sum_module],
       py_modules = ["min_max_sum"],
       )