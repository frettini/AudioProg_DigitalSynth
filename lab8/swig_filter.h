// File: min_max_sum.h
//
// Given an array of doubles, return its minimum and
// maximum values and the sum of its contents in
// diverse and amusing ways.
//
// A2DD.h
#ifndef swig_filter_H
#define swig_filter_H

#include <cstddef>
#include <vector>
#include <iostream>


class Delay{
private:
        int m_n = 2;
public:
        int hello = 1;
        double m_processArr[2];
        Delay(int delaySize);
        void process(double audioSample);
};

class Filter{
        
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
        Delay d;
};

class Test{
public:
        Test(const double* in, std::size_t in_size);
};


#endif