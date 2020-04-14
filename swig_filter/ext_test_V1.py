import numpy as np

import swig_filter as sf


coefs = np.random.rand(3,6)

# coefs = np.concatenate((coefs,coefs2))
print(coefs)

# inst a delay, gain and filter object
# pole magnitude distance to 1 = Q 
# difference between zero and poles = gain
filt_bank = sf.FilterChain(coefs)
filt_bank.setCoef(coefs)

# Generate and filter the buffer
white_buffer = np.random.rand(1000)
result = np.zeros(len(white_buffer))

filt_bank.genBuffer(result, np.array(white_buffer)) # filter it 



print("Success: you made it up to here")
print("Danke Schon")

filt_bank = None