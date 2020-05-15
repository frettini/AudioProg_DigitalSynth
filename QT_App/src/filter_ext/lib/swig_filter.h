// File: min_max_sum.h
//
// Given an array of doubles, return its minimum and
// maximum values and the sum of its contents in
// diverse and amusing ways.
//
// A2DD.h
#ifndef swig_filter_H
#define swig_filter_H

#include "delay.h"


// abstract base class
class Modifier{
private:
        float sampleRate;

public:
        virtual void modBuffer(double* out, std::size_t out_size,
                          const double* in, std::size_t in_size) = 0;

};


class Filter: public Modifier{
public:
                
        // define constructor
        Filter(const double* in, std::size_t in_size);
        
        // set coefficient at any time
        void setCoef(const double* in, std::size_t in_size);
        
        // modify the buffer, derived from modifier
        void modBuffer(double* out, std::size_t out_size,
                          const double* in, std::size_t in_size);

private:
        double m_a[3];
        double m_b[3];
        Delay d;
};


class FilterChain: public Modifier{
private:
        size_t size;
        std::vector<Filter> filterBank;

public:
        FilterChain(const double* in, 
                        std::size_t in_size1, 
                        std::size_t in_size2);

        void modBuffer(double* out, std::size_t out_size,
                          const double* in, std::size_t in_size);

        void setCoef(const double* in, 
                        std::size_t in_size1, 
                        std::size_t in_size2);

        void addFilter(const double* in , std::size_t in_size);
        void removeFilter();

};




#endif