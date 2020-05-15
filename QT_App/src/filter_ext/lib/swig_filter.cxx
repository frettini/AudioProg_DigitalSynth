#include <algorithm>
#include "swig_filter.h"



// Filter init----------------------------------------------------------------------------
//pass the coefficient
Filter::Filter(const double* in, std::size_t in_size): d(2){
    setCoef(in, in_size);
};

void Filter::setCoef(const double* in, std::size_t in_size){
    //implementation of the filter

    for(size_t i = 0; i<in_size; i++){
        if (i<3){
            m_a[i] = *(in+i);
        }else{
            m_b[i-3] = *(in+i);
        }
    }     
};

void Filter::modBuffer(double* out, std::size_t out_size, const double* in, std::size_t in_size){
    double middle = 0;
    double result = 0;
    
    for(size_t i = 0; i<in_size; i++){
        
        middle = *(in+i) - m_b[1]* d.get(0) - m_b[2] * d.get(1);
        result = middle * m_a[0] + m_a[1]* d.get(0) + m_a[2]* d.get(1);
        
        // if(result > 1.5) d.reset();
        d.process(middle);
        *(out+i) = result;
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

void FilterChain::modBuffer(double* out, std::size_t out_size,
                          const double* in, std::size_t in_size){
    
    for (size_t i = 0; i < size; i++)
    {
        filterBank[i].modBuffer(out, out_size, in, in_size);
    }
};

void FilterChain::setCoef(const double* in, 
                            std::size_t in_size1, 
                            std::size_t in_size2){
    if(size > in_size1){
        for(size_t i = 0; i < (size - in_size1); i++){
            removeFilter();
        }
        size = in_size1;
    }

    for (size_t i = 0; i < in_size1; i++)
    {
        // add filter here (coefficient needs to be known)
        if(i >= size){

            addFilter(in+i*in_size2, in_size2);
            size = i;
            continue;
        }

        filterBank[i].setCoef(in+i*in_size2, in_size2);
    }
    
};


void FilterChain::addFilter(const double* in, std::size_t in_size){
    std::cout << "Add Filter \n ";
    filterBank.push_back(Filter(in, in_size));
    std::cout << "vector size: " << filterBank.size() << "\n ";

};

void FilterChain::removeFilter(){
    std::cout << "Remove Filter \n ";
    filterBank.pop_back();
    std::cout << "vector size: " << filterBank.size() << "\n ";

};
