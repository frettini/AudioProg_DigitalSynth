# needed to import a module when it is not contained within a package
# used now as the swig filter is maintained at a top level
# might be better to wrap the application in a pacakge or move swig_fitler with the modules
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
import swig_filter as sf
import numpy as np

print("hello world")

coefs = np.array([[0,0,0,0,0,0], [1,1,1,1,1,1]])
sf.FilterChain(coefs)
