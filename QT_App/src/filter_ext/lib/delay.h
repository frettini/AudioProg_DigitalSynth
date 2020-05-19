#ifndef delay_H
#define delay_H

#include <iostream>
#include <cstddef>
#include <vector>

class Delay{
public:
        Delay(int delaySize);     
        
        // delay function 
        void process(double sample);
        void reset();
        // get a value from the delay vector
        double get(int ind);
        void printArray();
private :
        int size;
        std::vector<double> m_processVect;
};


#endif
