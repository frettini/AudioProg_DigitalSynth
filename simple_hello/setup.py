#!/usr/bin/env python

"""
setup.py file for SWIG example
"""

from distutils.core import setup, Extension


simple_hello_module = Extension('_simple_hello',
                           sources=['simple_hello_wrap.cxx', 'simple_hello.cxx'],
                           )

setup (name = 'simple_hello',
       version = '0.1',
       author      = "SWIG Docs",
       description = """simple hello test""",
       ext_modules = [simple_hello_module],
       py_modules = ["simple_hello"],
       )