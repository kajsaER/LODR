#!/usr/bin/python


import math
from .Support_Files import constants as consts
from .Support_Files import extmath

sea = 0
high = 6

class atmosphere:

    def __init__(self):
        self.__Teff = 0.5           # Transmission efficiency
        self.__lambdaref = 1e-6     # Reference wavelenght
        self.__thetarefhigh = 2e-6  # Reference turbulence divergency
        self.__thetarefsea = 9e-6   #  angle, sea and high altitude
        self.__alt = high           # Altitude of Gs
        # The parameters needed to discribe the atmosphere, some might be random

    def setalt(self, level):        # Set altitude
        if level == sea or level == high:   # Known values
            self.__alt = level
        else:                       # Unknown value
            print("Elevation level unknown")

    def Teff(self):         # Get transmission efficiency
        return self.__Teff

    # Turbulence
    def turbulence(self, lam):  # Get turbulence divergency angle
        if self.__alt == sea:   # Use sea or high altitude values?
            thetaref = self.__thetarefsea
        else:
            thetaref = self.__thetarefhigh
        
        return thetaref * math.pow(self.__lambdaref / lam, 0.2)

    # Stimulated Raman Scattering


    # Jitter
    def jitter(self):       # Neglected for now
        return 0 # theta_jitter

    # Thermal bloomimg
    def bloom(self):        # Neglected for now
        return 0 # theta_bloom


    # Total atmospheric diversion
    def divergence2(self, lam): # Calculate and return θ²atm
        return math.pow(self.turbulence(lam), 2) + math.pow(self.jitter(), 2) + math.pow(self.bloom(), 2)
