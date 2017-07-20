#!/usr/bin/python

class laser:

    def __init__(self, power, wavelength):
        self.P = power #Power
        self.lambd = wavelength #Wavelength

    

    def __del__(self):
        print "Laser has been deleted"


class beam:
    def __init__(self, lam, a, Deff, M2, W):
        self._lambda = lam # Wavelength
        self._a = a # Beam coefficient
        self._Deff = Deff # Illuminated beam diameter
        self._M2 = M2 # Beam quality factor
        self._W = W # Pulse energy
    
    def __del__(self):
        print "Beam terminated"
