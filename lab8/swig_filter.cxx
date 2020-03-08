#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "swig_filter.h"


PyMethodDef swig_filter_Methods[]=
{
    {0,0,0,0}
};


static struct PyModuleDef swig_filter_module = {
    PyModuleDef_HEAD_INIT,
    "swig_filter",   /* name of module */
    "swig_filter_doc", /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    swig_filter_Methods
};


PyMODINIT_FUNC 
PyInit_example(void)
{
    return PyModule_Create(&swig_filter_module);
}


// return the min, max and sum of the given array.
// SWIG will arrange for this to be returned as a tuple.
        
void MMS::mms_t(const double* in, std::size_t in_size, double* min, double* max, double* sum)
{
    
    
};


        
// return the min, max and sum of the given numpy array 'in'.
// SWIG will write the values into the given numpy array, 'out'.
void MMS::mms_a(double* out, std::size_t out_size, const double* in, std::size_t in_size)
{
    
};


