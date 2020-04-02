#ifndef swig_filter_H
#define swig_filter_H

class Delay{
public:
        

        Delay(int delaySize);           // constructor
        
        void process(double sample);
        void reset();
        double get(int ind);
        void printArray();
private :
        int size;
        std::vector<double> m_processVect;
};


#endif
