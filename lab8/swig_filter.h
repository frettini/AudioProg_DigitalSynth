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
public:
        

        Delay(int delaySize);           // constructor
        Delay(const Delay &obj);        // copy constructor
        ~Delay();                       // destructor

        void process(double sample);
        double get(int ind);
        void printArray();
private:
        int size;
        double* m_processArr;
        std::vector<double> m_processVect;
};


class Filter{
public:
        Delay d; //cant be private for some reason
                
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
        
};

class FilterChain{
public:
        std::vector<Filter> filterBank;

        FilterChain(const double* in, 
                        std::size_t in_size1, 
                        std::size_t in_size2);

        void genBuffer(double* out, std::size_t out_size,
                          const double* in, std::size_t in_size);
};


#endif