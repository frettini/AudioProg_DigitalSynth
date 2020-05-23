#!/usr/bin/env python

"""
setup.py file for the tone generator
"""

# system import
# from distutils.core import setup, Extension
from setuptools import setup, Extension
import os

# 3rd party module
import numpy


#-----------------------------------------------------------------------------------
# SETUP
# Specify the name of the extension, version and author name here
name = "swig_filter"
author = "Nicolae Marton"
version = "0.1"
description = """Modules that implements audio filters in C"""
# output directory for the extension
target_Dir = os.path.join("src", "filter_ext")
# include and lib directory
# srcDir = os.path.abspath('./src')
srcDir = os.path.join("src", "filter_ext")
#-----------------------------------------------------------------------------------


# Obtain the numpy include directory.  This logic works across numpy versions.
try:
    numpy_include = numpy.get_include()
except AttributeError:
    numpy_include = numpy.get_numpy_include()

# create the module, and interface names
mod_name = "_" + name
interface = name + ".i"

# add package target directory
mod_name = target_Dir + "." + mod_name
interface = os.path.join(target_Dir,interface)


# initialize source which contains all the files to compile
# initialize swig options which will contain includes
# initialize include directories which will contain the external and local includes
srcFiles = [interface] 
swig_opts = ['-c++', '-modern'] 
include_dirs = [numpy_include]

# get absolute path for each subdirectory
# add the subdir to the include directories
for root, dirs, files in os.walk(srcDir):
    for dir in dirs:
        full_path = os.path.join(srcDir, dir)
        swig_opts += ["-I" + full_path]
        include_dirs += [full_path]

# get all cxx and c files in the lib directory
# add them to the source files to be compiled
for file in os.listdir(os.path.join(srcDir,'lib')):
    if file.endswith(".cxx") or file.endswith(".c"):
        srcFiles += [os.path.join(srcDir,'lib',file)]


# create the python extension
# specify swig options 
swig_module = Extension(mod_name, 
                           sources=srcFiles,
                           swig_opts = swig_opts
                           ) 

# create the extension setup
setup (name = name,
       version = version,
       author      = author,
       description =  description,
       ext_modules = [swig_module],
       py_modules = [name],
       include_dirs = include_dirs 
       )