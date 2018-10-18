#!/usr/bin/python

import math
from .orbit import orbit as Orbit
from .Support_Files import constants as consts
from .Support_Files import extmath
import matplotlib.pyplot as plt
import numpy as np


class debris:
    def __init__(self, ID, etac, Cm, size, mass, nu,
                 orbit=None, rp=None, ep=None, omega=None):
        self.ID = ID        # Identifier for the specific piece of debris
        self.compute(etac, Cm, size, mass, nu, orbit, rp, ep, omega)

    def compute(self, etac, Cm, size, mass, nu,     # Calculate and set 
                orbit=None, rp=None, ep=None, omega=None):  # all variables
        self.__Transfer = np.empty(shape=(0,2))     # Empty matrix for transfer
        self._Cm = Cm           # Momentum coupling coefficient
        self._orbit = orbit     # Orbit
        self._size = size       # Debris radius in m
        self._mass = mass       # Debris mass in kg
#        self._orientation = orientation   # Not used for assumed spherical debris
        if orbit != None:       # If an orbit was provided, use it
            self._orbit = orbit
        else:                   # If no orbit was provided, make one
            self._orbit = Orbit()
            self._orbit.make(rp, ep, omega)
        self._nu = nu           # True anomaly
        self._etac = etac       # Combined coefficiency factor
        self._snu = math.sin(self._nu)
        self._cnu = math.cos(self._nu)
        self._r = (self._orbit.a*(1- math.pow(self._orbit.ep, 2)) / 
                   (1+self._orbit.ep*self._cnu))    # Orbital radius
        self._v = math.sqrt(consts.mu*(2/self._r - 1/self._orbit.a))*1.0    # Velocity
        self._sgamma = self._orbit.rp*self._orbit.vp / (self._r*self._v)    # ∠rv
        self._cgamma = math.sqrt(1 - math.pow(self._sgamma, 2))     # cos(γ) ≥ 0
        if self._nu < math.pi:      # If ν < π then cos(γ) < 0
            self._cgamma = - self._cgamma

    def step(self):                 # Take a step along the orbit
        dnu = (self._orbit.a*self._orbit.b*self._orbit.n /  # Δν = a*b*n/r²
               math.pow(self._r, 2))
        vp = self._orbit.vp         # Velocity at perigee
        self._nu = self._nu + dnu   
        if self._nu > 2*math.pi:    # Make ν ∈ [0, 2π)
            self._nu -= 2*math.pi
        elif self._nu < 0:
            self._nu += 2*math.pi
        self._snu = math.sin(self._nu)
        self._cnu = math.cos(self._nu)
        self._r = (self._orbit.a*(1- math.pow(self._orbit.ep, 2)) / 
                   (1+self._orbit.ep*self._cnu))    # r = a(1-ε²)/(1-ε cos(ν))
        self._v = math.sqrt(consts.mu*(2/self._r - 1/self._orbit.a))*1.0    #Vis-viva
        self._sgamma = self._orbit.rp*vp / (self._r*self._v)    # Law of Sines

        if self._sgamma > 1:        # Impossible γ causes exception
            raise Exception("Sin gamma = " + repr(self._sgamma) + ".\n" +
                            "vp = " + repr(self.vp) + "  v = " + repr(self._v) + ".\n" +
                            "rp = " + repr(self._orbit.rp) + "  r = " + repr(self._r))
        
        self._cgamma = math.sqrt(1 - math.pow(self._sgamma, 2)) # Pythagorean trigonometric identity
        
        if self._nu < math.pi:      # If ν < π then γ ∈ [π/2, 3π/2]
            self._cgamma = - self._cgamma

    def measure(self):          # Calculate and return values as measured from Gs
        snuw = extmath.sinplus(self._orbit.sw, self._orbit.cw,  # ν+ω
                               self._snu, self._cnu)
        cnuw = extmath.cosplus(self._orbit.sw, self._orbit.cw,
                               self._snu, self._cnu)
        cphi = extmath.cosminus(snuw, cnuw, consts.slat, consts.clat)   # φ = ν + ω - ∅
        sphi = extmath.sinminus(snuw, cnuw, consts.slat, consts.clat) 
        z = math.sqrt(math.pow(consts.Re, 2) + math.pow(self._r, 2)
                      - 2*consts.Re*self._r*cphi)       # Law of Cosines
        cdelta = (math.pow(self._r, 2) + math.pow(z, 2) - math.pow(consts.Re, 2)) / (2*self._r*z)
        sdelta = consts.Re/z*(-sphi)                    # Law of Sines
        calpha = (math.pow(consts.Re, 2) + math.pow(z, 2) - math.pow(self._r, 2)) / (2*consts.Re*z)
        salpha = self._r/z*(-sphi)
        cbeta = extmath.cosminus(salpha, calpha, 1, 0)  # β = α - π/2
        sbeta = extmath.sinminus(salpha, calpha, 1, 0)
        szeta = extmath.sinminus(self._sgamma, self._cgamma, sdelta, cdelta)    # ζ = γ - δ
        czeta = extmath.cosminus(self._sgamma, self._cgamma, sdelta, cdelta)
        return{'z':z, 'v':self._v, 'szeta':szeta, 'czeta':czeta,
                'sbeta':sbeta, 'cbeta':cbeta, 'sdelta':sdelta,
                'cdelta':cdelta, 'sphi':sphi, 'cphi':cphi}

    def get_beta(self):         # Calculate and return the elevation angle
        snuw = extmath.sinplus(self._orbit.sw, self._orbit.cw, self._snu, self._cnu)
        cnuw = extmath.cosplus(self._orbit.sw, self._orbit.cw, self._snu, self._cnu)
        cphi = extmath.cosminus(snuw, cnuw, consts.slat, consts.clat) 
        sphi = extmath.sinminus(snuw, cnuw, consts.slat, consts.clat) 
        z = math.sqrt(math.pow(consts.Re, 2) + math.pow(self._r, 2) - 2*consts.Re*self._r*cphi)
        calpha = (math.pow(consts.Re, 2) + math.pow(z, 2) - math.pow(self._r, 2)) / (2*consts.Re*z)
        salpha = self._r/z*(-sphi)
        cbeta = extmath.cosminus(salpha, calpha, 1, 0)  # β = α - π/2
        sbeta = extmath.sinminus(salpha, calpha, 1, 0)
        return math.atan2(sbeta, cbeta)

    def plot_data(self):        # Calculate and return [x,y] coordinates
        X = self._r*extmath.cosplus(self._orbit.sw, self._orbit.cw, self._snu, self._cnu)
        Y = self._r*extmath.sinplus(self._orbit.sw, self._orbit.cw, self._snu, self._cnu)
        return [X, Y]

    def hit(self, Phi, szeta, czeta, reps): # Calculate and return v and ζ
        dvz = (reps*self._etac*self._Cm*Phi /       # velocity change in z
               (self._mass/(math.pi*math.pow(self._size, 2))))  # direction
        v = math.sqrt(math.pow((self._v - dvz*czeta), 2) + math.pow((dvz*szeta), 2))
        sdzeta = dvz*szeta/v
        cdzeta = (self._v - dvz*czeta) / v
        self._v = v*1.0
        szeta2 = extmath.sinplus(szeta, czeta, sdzeta, cdzeta)
        czeta2 = extmath.cosplus(szeta, czeta, sdzeta, cdzeta)
        return np.array([szeta2, czeta2, v])

    def transfer(self):         # Add coordinates to transfer matrix
        self.__Transfer = np.vstack((self.__Transfer, self.plot_data()))

    def transfer_data(self):    # Get transfer data and reset matrix
        self.transfer()
        Temp = self.__Transfer
        self.__Transfer = np.empty(shape=(0,2))
        return Temp

