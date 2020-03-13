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
};

// initializer definition
Delay::Delay(int delaySize): m_n(delaySize) {
    std::cout << "  delay constructor start  ";
    for(int i = 0; i<m_n; i++){
        m_processArr[i] = 0;
    }
    std::cout << "  end  ";
    // m_processArr1 = 0;
    // m_processArr2 = 0;
};

void Delay::process(double audioSample){
    // m_processArr2 = m_processArr1;
    // m_processArr1 = audioSample;

    m_processArr[1] = m_processArr[0]; 
    m_processArr[0] = audioSample;
};

//pass the coefficient
Filter::Filter(const double* in, std::size_t in_size): d(2){
    std::cout << "  constructor  ";
    setCoef(in, in_size);
};

void Filter::setCoef(const double* in, std::size_t in_size){
    //implementation of the filter
    for(int i = 0; i<in_size; i++){
        if(i<3) this->m_a[i] = *(in+i);
        else this->m_b[i] = *(in+i);
    }     
};

void Filter::genBuffer(double* out, std::size_t out_size, const double* in, std::size_t in_size){
    std::cout << "start genbuffer";
    double middle = 0;
    double result = 0;
    
    for(int i = 0; i<in_size; i++){
        middle = *(in+i) - m_b[1]* d.m_processArr[0] - this->m_b[2] * d.m_processArr[1];
        *(out+i) = middle * this->m_a[0] + m_a[1]* d.m_processArr[0] + this->m_a[2]*d.m_processArr[1];
        d.process(middle);
    }
};

Test::Test(const double* in, std::size_t in_size){
    std::cout << in;
};


