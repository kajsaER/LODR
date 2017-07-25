#!/usr/bin/python

import math
import extmath

class laser:

    def __init__(self, power, wavelength):
        self.P = power #Power
        self.lambd = wavelength #Wavelength

    

    def __del__(self):
        print "Laser has been deleted"


class beam:
    def __init__(self, lam, a, Deff, M2, W, tau):
        self._lambda = lam # Wavelength
        self._a = a # Beam coefficient
        self._Deff = Deff # Illuminated beam diameter
        self._M2 = M2 # Beam quality factor
        self._W = W # Pulse energy
        self._tau = tau # Pulse width

    def fluence(self, z, Teff):
        return self._W*self._Deff*4*Teff / (math.pi*math.pow(self._M2*self._a*self._lambda, 2)*math.pow(z, 2))

    def spot(self, z):
        return self._a*self._M2*self._lambda*z / self._Deff
    
    def __del__(self):
        print "Beam terminated"
