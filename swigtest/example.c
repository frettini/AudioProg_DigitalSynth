/* File: example.c */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "example.h"

int fact(int n) {
    if (n < 0){ /* This should probably return an error, but this is simpler */
        return 0;
    }
    if (n == 0) {
        return 1;
    }
    else {
        /* testing for overflow would be a good idea here */
        return n * fact(n-1);
    }
}

PyMethodDef ExampleMethods[]=
{
    {0,0,0,0}
};


static struct PyModuleDef examplemodule = {
    PyModuleDef_HEAD_INIT,
    "Example",   /* name of module */
    "example_doc", /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    ExampleMethods
};


PyMODINIT_FUNC 
PyInit_example(void)
{
    return PyModule_Create(&examplemodule);
}


