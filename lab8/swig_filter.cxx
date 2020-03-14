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
Delay::Delay(int delaySize): m_processVect(delaySize, 0.0)  {
    std::cout << "delay constructor start \n ";
    
    std::cout << "end  \n";
};

void Delay::process(double audioSample){
    std::rotate(m_processVect.begin(), m_processVect.end()-1, m_processVect.end());
    m_processVect[0] = audioSample;
};

void Delay::printArray(){
    for (auto i = m_processVect.begin(); i != m_processVect.end(); ++i)
        std::cout << *i << ' ';
}

//pass the coefficient
Filter::Filter(const double* in, std::size_t in_size): d(2){
    std::cout << "constructor  \n";
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
    std::cout << "start genbuffer  \n";
    double middle = 0;
    double result = 0;
    
    for(int i = 0; i<in_size; i++){
        middle = *(in+i) - m_b[1]* d.m_processVect[0] - this->m_b[2] * d.m_processVect[1];
        *(out+i) = middle * this->m_a[0] + m_a[1]* d.m_processVect[0] + this->m_a[2]*d.m_processVect[1];
        d.process(middle);
    }
};



