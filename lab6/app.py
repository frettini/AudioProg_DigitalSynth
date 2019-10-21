from modules import complexcal
import math

pi = math.pi
c = complexcal.ComplexCal

magnitude, angle = c.multiplication(c, 4, pi/3, 3, pi/2)

print(magnitude)
print(angle)