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
    m_processArr = new double[size];

    //initialize the array with 0!
    for(int i = 0; i < size ; i++){
        *(m_processArr+i) = 0.0;
    }
};

Delay::Delay(const Delay &obj){
    //copy constructor
    std::cout << "Delay: copy constructor \n ";
    m_processArr = new double[obj.size];
    size = obj.size;
    // copy n characeter from source (obj.m_processArr) to dest (m_processArr)
    memcpy(m_processArr, obj.m_processArr, sizeof(double) * size); 
};

Delay::~Delay(){
    std::cout << "Delay: destructor \n ";
    delete [] m_processArr;
};


void Delay::process(double sample){
    // preferred way is to use vector with rotate, but the vector crashes the code
    std::rotate(m_processVect.begin(), m_processVect.end()-1, m_processVect.end());
    m_processVect[0] = sample;
    
    // for(int i = size-1; i > 0; --i){
    //     *(m_processArr+i) = *(m_processArr+i-1);
    // }
    // *m_processArr = sample;
};

double Delay::get(int ind){
    // return *(m_processArr + ind);
    return m_processVect[ind];
};

void Delay::printArray(){
    // for (int i = 0; i<size; i++)
    //     std::cout << *(m_processArr+i) << ' ';

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
        *(out+i) = middle * m_a[0] + m_a[1]* d.get(0) + m_a[2]* d.get(1);
        // middle = *(in+i) - m_b[1]* *(d.m_processArr) - m_b[2] * *(d.m_processArr+1);
        // *(out+i) = middle * m_a[0] + m_a[1]* *(d.m_processArr) + m_a[2]* *(d.m_processArr+1);
        d.process(middle);
    }
};



// FilterChain ----------------------------------------------------
FilterChain::FilterChain(const double* in, 
                        std::size_t in_size1, 
                        std::size_t in_size2): filterBank() {

    std::cout << "number of filters : " << in_size1 << "\n";
    
    filterBank.reserve(in_size1);

    for(int i = 0; i < in_size1; i++){
        filterBank.push_back(Filter(in+i, in_size2));
    }

};

void FilterChain::genBuffer(double* out, std::size_t out_size,
                          const double* in, std::size_t in_size){


};

