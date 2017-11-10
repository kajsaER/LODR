#!/usr/bin/python

import math
import extmath
import constants as consts
import numpy as np

class laser:

    def __init__(self):
        self._powers = np.array([70.0, 2.0, 5.0]) # Array of powers of different lasers
        self._lambdas = np.array([10.6e-6, 1.06e-6, 830e-9]) # Array of wavelengths of different lasers
        self._M2s = np.array([2, 2, 2]) # Array of beam quality factors for different lasers

        self._type = 0 # The index of the chosen laser
        self._P = self._powers[0]#The power of the chosen laser
        self._lambda = self._lambdas[0] #The wavelength of the chosen laser
        self._M2 = self._M2s[0] # The beam quality factor of the chosen laser
        self._Cb = 1.9 # Beam coefficient

        self._dubf = False
        self._tau = 5e-7
        self._frep = 10e3
        self._W = self._P/self._frep
#        print "W = " + repr(self._W)

    def switch(self, i):
        self._P = self._powers[i]
        self._lambda = self._lambdas[i]
        self._type = i
        if self._dubf == True:
            self._lambda = 2*self._lambda

    def doubfreq(self):
        self._dubf = True
        self._lambda = self._lambdas[self._type]/2

    def normfreq(self):
        self._dubf = False
        self._lambda = self._lambdas[self._type]

    def spot(self, z, Deff, atm):
        diveff = self.div(Deff, atm)
        return 2 * diveff * z
    
    def fluence(self, z, Deff, atm):
        diveff = self.div(Deff, atm)
        return self._W*atm.Teff() / (math.pi*math.pow(diveff, 2)*math.pow(z, 2))

    def div(self, Deff, atm):
        divM2 = self._M2 * self._Cb/4 * self._lambda/(Deff/2)
        return math.sqrt(math.pow(divM2, 2) + atm.divergence2(self._lambda))

    def fire(self, ant, deb, duration, atm):
        meas = deb.measure()
        z = meas['z']
        szeta = meas['szeta']
        czeta = meas['czeta']
        sgamma = meas['sgamma']
        cgamma = meas['cgamma']
        sdelta = meas['sdelta']
        cdelta = meas['cdelta']
        sphi = meas['sphi']
        cphi = meas['cphi']
        if duration <= 1:
            debval = deb.hit(self.spot(z, ant.Deff(), atm), self.fluence(z, ant.Deff(), atm), szeta, czeta, self._frep*duration)
            szeta = debval[0]
            czeta = debval[1]
            v = debval[2]
        else :
            debval = deb.hit(self.spot(z, ant.Deff(), atm), self.fluence(z,ant.Deff(), atm), szeta, czeta, self._frep)
            szeta = debval[0]
            czeta = debval[1]
            v = debval[2]
        duration -= 1
        deb._orbit.find(z, v, szeta, czeta, sgamma, cgamma)
        sw = deb._orbit.sw
        cw = deb._orbit.cw
        spw = extmath.sinplus(sphi, cphi, sw, cw)
        cpw = extmath.cosplus(sphi, cphi, sw, cw)
        deb._snu = extmath.sinminus(consts.slat, consts.clat, spw, cpw)
        deb._cnu = extmath.cosminus(consts.slat, consts.clat, spw, cpw)
        deb._nu = math.atan2(deb._snu, deb._cnu)
        if deb._nu < 0:
            deb._nu += 2*math.pi
        deb._stheta = extmath.sinplus(sdelta, cdelta, szeta, czeta)
        deb._ctheta = extmath.cosplus(sdelta, cdelta, szeta, czeta)
        if duration > 0:
            deb.step()
            self.fire(ant, deb, duration, atm)
 
    def __del__(self):
        print "Laser has been deleted"

