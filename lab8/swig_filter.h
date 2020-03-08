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

class MMS {
public:
        // return the min, max and sum of the given array.
        // SWIG will arrange for this to be returned as a tuple.
        static void mms_t(const double* in, std::size_t in_size,
                          double* min, double* max, double* sum);

        // return the min, max and sum of the given numpy array 'in'.
        // SWIG will write the values into the given numpy array, 'out'.
        static void mms_a(double* out, std::size_t out_size,
                          const double* in, std::size_t in_size);
};


#endif