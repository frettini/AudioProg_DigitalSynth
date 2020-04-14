import os

# 3rd party module
import numpy

# Obtain the numpy include directory.  This logic works across numpy versions.
try:
    numpy_include = numpy.get_include()
except AttributeError:
    numpy_include = numpy.get_numpy_include()


name = "swig_filter"

# create the file names and modules names
mod_name = "_" + name
wrapper = name + ".i"
interface = name + "_wrap.cpp"

srcFiles = [interface, wrapper]
swig_opts = ['-c++', '-modern']
include_dirs = [numpy_include]

srcDir = os.path.abspath('src')

for root, dirs, files in os.walk(srcDir):

    for dir in dirs:
        full_path = os.path.join(srcDir, dir)
        swig_opts += ["-I" + full_path]
        include_dirs += [full_path]


for file in os.listdir(os.path.join(srcDir,'lib')):
    if file.endswith(".cxx") or file.endswith(".c"):
        srcFiles += [os.path.join(srcDir,'lib',file)]


print(srcFiles)
print(swig_opts)
print(include_dirs)