#!/usr/bin/python


import math
from . import Support_Files
#from . import Support_Files.constants as consts

sea = 0
high = 6

class atmosphere:

    def __init__(self):
        self.__Teff = 0.5
        self.__lambdaref = 1e-6
        self.__thetarefhigh = 2e-6
        self.__thetarefsea = 9e-6
        self.__alt = high
        # The parameters needed to discribe the atmosphere, some might be random

    def setalt(self, level):
        if level == sea or level == high:
            self.__alt = level
        else:
            print("Elevation level unknown")

    def Teff(self):
        return self.__Teff

    # Turbulence
    def turbulence(self, lam):
        if self.__alt == sea:
            thetaref = self.__thetarefsea
        else:
            thetaref = self.__thetarefhigh
        
        return thetaref * math.pow(self.__lambdaref / lam, 0.2) # theta_turb

    # Stimulated Raman Scattering


    # Jitter
    def jitter(self):
        return 0 # theta_jitter

    # Thermal bloomimg
    def bloom(self):
        return 0 # theta_bloom


    # Total atmospheric diversion
    def divergence2(self, lam):
        return math.pow(self.turbulence(lam), 2) + math.pow(self.jitter(), 2) + math.pow(self.bloom(), 2)
