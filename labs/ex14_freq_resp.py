from modules import complexcal
import matplotlib.pyplot as plot
import numpy as np
import math

pi = math.pi
c = complexcal.ComplexCal




def frequency_response(poles, zeros):
    print(poles)
    print(zeros)

    gmag_arr = np.array([])
    gang_arr = np.array([])

    #alpha ranges from 0 to 1 
    for alpha in np.arange(0,1.0,0.001):
        p1mag, p1ang = c.substract(c, 1, alpha*2*pi, poles[0], poles[1])
        p2mag, p2ang = c.substract(c, 1, alpha*2*pi, poles[2], poles[3])

        z1mag, z1ang = c.substract(c, 1, alpha*2*pi, zeros[0], zeros[1])
        z2mag, z2ang = c.substract(c, 1, alpha*2*pi, zeros[2], zeros[3])

        pmag, pang = c.multiplication(c, p1mag, p1ang, p2mag, p2ang)
        zmag, zang = c.multiplication(c, z1mag, z1ang, z2mag, z2ang)

        gmag, gang = c.division(c, zmag, zang, pmag, pang)
        gmag_arr = np.append(gmag_arr, gmag)
        gang_arr = np.append(gang_arr, gang)

    plot.plot(gmag_arr)
    plot.show()
        


    
    # calculate response for a bunch of alpha,
    # then plot them

poles = np.array([0.8, 0.62689, 0.8, -0.62689])
zeros = np.array([0.9, 0.62689, 0.9, -0.62689])
frequency_response(poles, zeros)
