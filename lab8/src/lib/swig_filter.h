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

// #include <cstddef>
// #include <vector>
// #include <iostream>



// class Delay{
// public:
        

//         Delay(int delaySize);           // constructor
        
//         void process(double sample);
//         void reset();
//         double get(int ind);
//         void printArray();
// private :
//         int size;
//         std::vector<double> m_processVect;
// };


class Generator{
private:
        float sampleRate;

public:
        virtual void genBuffer(double* out, std::size_t out_size,
                          const double* in, std::size_t in_size) = 0;

};

class Filter: public Generator{
public:
                
        // define constructor
        Filter(const double* in, std::size_t in_size);
        
        // set coefficient at any time
        void setCoef(const double* in, std::size_t in_size);
        
        // generate the buffer (should derive from gen)
        void genBuffer(double* out, std::size_t out_size,
                          const double* in, std::size_t in_size);

private:
        double m_a[3];
        double m_b[3];
        // double m_delayArr[2];
        Delay d;
};

class FilterChain: public Generator{
private:
        size_t size;
        std::vector<Filter> filterBank;

public:
        FilterChain(const double* in, 
                        std::size_t in_size1, 
                        std::size_t in_size2);

        void genBuffer(double* out, std::size_t out_size,
                          const double* in, std::size_t in_size);

        void setCoef(const double* in, 
                        std::size_t in_size1, 
                        std::size_t in_size2);
};




#endif