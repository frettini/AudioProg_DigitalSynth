import math

class ComplexCal:

    def __init__(self):
        pass

    def add(self, mag1, ang1, mag2, ang2):
        x1 = mag1 * math.cos(ang1)
        x2 = mag2 * math.cos(ang2)
        y1 = mag1 * math.sin(ang1)
        y2 = mag2 * math.sin(ang2)

        x = x1 + x2
        y = y1 + y2

        magnitude = math.sqrt(x**2 + y**2)
        angle = math.atan(y/x)

        return magnitude, angle

    def multiplication(self, mag1, ang1, mag2, ang2):
        
        magnitude = mag1*mag2
        angle = ang1 + ang2

        return magnitude, angle

    def division(self, mag1, ang1, mag2, ang2):
        
        magnitude = mag1/mag2
        angle = ang1 - ang2
        
        return magnitude, angle