// Delay init ----------------------------------------------------------------------------------------
Delay::Delay(int delaySize): size(delaySize), m_processVect(size, 0.0)  {
    std::cout << "Delay: constructor start \n ";
    
};


void Delay::process(double sample){
    // preferred way is to use vector with rotate, but the vector crashes the code
    std::rotate(m_processVect.begin(), m_processVect.end()-1, m_processVect.end());
    m_processVect[0] = sample;
};

void Delay::reset(){
    for(int i = 0; i < size; i++){
        m_processVect[i] = 0.0;
    }
}

double Delay::get(int ind){
    return m_processVect[ind];
};

void Delay::printArray(){
    for (auto i = m_processVect.begin(); i != m_processVect.end(); ++i)
        std::cout << *i << ' ';
};