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



// Delay init ----------------------------------------------------
Delay::Delay(int delaySize): size(delaySize), m_processVect(size, 0.0)  {
    std::cout << "Delay: constructor start \n ";
    
};


void Delay::process(double sample){
    // preferred way is to use vector with rotate, but the vector crashes the code
    std::rotate(m_processVect.begin(), m_processVect.end()-1, m_processVect.end());
    m_processVect[0] = sample;
};

void Delay::reset(){
    for(int i = 0; i < size; i++){
        m_processVect[i] = 0.0;
    }
}

double Delay::get(int ind){
    return m_processVect[ind];
};

void Delay::printArray(){
    for (auto i = m_processVect.begin(); i != m_processVect.end(); ++i)
        std::cout << *i << ' ';
};




// Filter init----------------------------------------------------
//pass the coefficient
Filter::Filter(const double* in, std::size_t in_size): d(2){
    std::cout << "Filter: constructor  \n";
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
    std::cout << "Filter: start genbuffer  \n";
    double middle = 0;
    double result = 0;
    
    for(int i = 0; i<in_size; i++){
        middle = *(in+i) - m_b[1]* d.get(0) - m_b[2] * d.get(1);
        result = middle * m_a[0] + m_a[1]* d.get(0) + m_a[2]* d.get(1);
        
        if(result > 1.5) d.reset();
        d.process(middle);
        *(out+i) = result;
    }
};



// FilterChain ----------------------------------------------------
FilterChain::FilterChain(const double* in, 
                        std::size_t in_size1, 
                        std::size_t in_size2): filterBank() {

    std::cout << "number of filters : " << in_size1 << "\n";
    size = in_size1;
    filterBank.reserve(in_size1);

    for(int i = 0; i < in_size1; i++){
        filterBank.push_back(Filter(in+i*in_size2, in_size2));
    }

};

void FilterChain::genBuffer(double* out, std::size_t out_size,
                          const double* in, std::size_t in_size){
    for (size_t i = 0; i < size; i++)
    {
        std::cout << "FC: generate buff: " << i << "\n";
        filterBank[i].genBuffer(out, out_size, in, in_size);
    }

};

