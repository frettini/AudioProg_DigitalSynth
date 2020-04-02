// File: simple_hello.cxx
//
Implementation of the Hello function suite in C++
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <iostream>
#include <string>

#include "simple_hello.h"

int hw(int x, int y)
{
    return x + y;
}

PyMethodDef shMethods[]=
{
    {0,0,0,0}
};


static struct PyModuleDef shmodule = {
    PyModuleDef_HEAD_INIT,
    "simple_hello",   /* name of module */
    "simple_hello_doc", /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    shMethods
};


PyMODINIT_FUNC 
PyInit_example(void)
{
    return PyModule_Create(&shmodule);
}
