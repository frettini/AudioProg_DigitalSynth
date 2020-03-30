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



// Filter init----------------------------------------------------
//pass the coefficient
Filter::Filter(const double* in, std::size_t in_size){
    setCoef(in, in_size);
    m_delayArr[0] = 0.0;
    m_delayArr[1] = 0.0;
};

void Filter::setCoef(const double* in, std::size_t in_size){
    //implementation of the filter

    for(int i = 0; i<in_size; i++){
        if (i<3){
            m_a[i] = *(in+i);
        }else{
            m_b[i-3] = *(in+i);
        }
    }     


};

void Filter::genBuffer(double* out, std::size_t out_size, const double* in, std::size_t in_size){
    double middle = 0;
    double result = 0;
    
    for(int i = 0; i<in_size; i++){
        middle = *(in+i) - m_b[1]* m_delayArr[0] - m_b[2] * m_delayArr[1];
        result = middle * m_a[0] + m_a[1]* m_delayArr[0] + m_a[2]* m_delayArr[1];
        
        // if(result > 1.5){
        //     m_delayArr[1] = 0.0;
        //     m_delayArr[0] = 0.0;
        // }

        *(out+i) = result;

        m_delayArr[1] = m_delayArr[0];
        m_delayArr[0] = middle;
    }
};



// FilterChain ----------------------------------------------------
FilterChain::FilterChain(const double* in, 
                        std::size_t in_size1, 
                        std::size_t in_size2): filterBank() {

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
        filterBank[i].genBuffer(out, out_size, in, in_size);
    }
};

void FilterChain::setCoef(const double* in, 
                            std::size_t in_size1, 
                            std::size_t in_size2){
    for (int i = 0; i < size; i++)
    {
        filterBank[i].setCoef(in+i*in_size2, in_size2);
    }
    
}
