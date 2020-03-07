#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "min_max_sum.h"


PyMethodDef min_max_sum_Methods[]=
{
    {0,0,0,0}
};


static struct PyModuleDef min_max_sum_module = {
    PyModuleDef_HEAD_INIT,
    "min_max_sum",   /* name of module */
    "min_max_sum_doc", /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    min_max_sum_Methods
};


PyMODINIT_FUNC 
PyInit_example(void)
{
    return PyModule_Create(&min_max_sum_module);
}


// return the min, max and sum of the given array.
// SWIG will arrange for this to be returned as a tuple.
        
void MMS::mms_t(const double* in, std::size_t in_size, double* min, double* max, double* sum)
{
    double temp_sum = 0;
    for(int i = 0; i<in_size; i++){
        temp_sum += *(in + i);
    }

    *sum = temp_sum;
    *min = 0;
    *max = 0;
};


        
// return the min, max and sum of the given numpy array 'in'.
// SWIG will write the values into the given numpy array, 'out'.
void MMS::mms_a(double* out, std::size_t out_size, const double* in, std::size_t in_size)
{

};


