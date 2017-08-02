#!/usr/bin/python

import math
import extmath
import constants as consts
import numpy as np

class laser:

    def __init__(self):
        self._powers = np.array([70.0, 2.0, 5.0])
        self._lambdas = np.array([10.6e-6, 1.06e-6, 830e-9])
        self._P = self._powers[0] #Power
        self._lambda = self._lambdas[0] #Wavelength

    def switch(self, i):
        self._P = self._powers[i]
        self._lambda = self._lambdas[i]

    def __del__(self):
        print "Laser has been deleted"


class beam:
    def __init__(self, laser, a, Deff, M2, tau, rep):
        self._laser = laser # Wavelength
        self._a = a # Beam coefficient
        self._Deff = Deff # Illuminated beam diameter
        self._M2 = M2 # Beam quality factor
        self._W = laser._P/(tau*rep)
        self._rep = rep

    def fire(self, deb, duration):
#        print "t: " + repr(duration) + " s"
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
#            print "Less than or eqaual to 1"
            debval = deb.hit(self.spot(z), self.fluence(z, 0.5), szeta, czeta, self._rep*duration)
            szeta = debval[0]
            czeta = debval[1]
            v = debval[2]
        else :
#            print "Greather than 1"
            debval = deb.hit(self.spot(z), self.fluence(z, 0.5), szeta, czeta, self._rep)
            szeta = debval[0]
            czeta = debval[1]
            v = debval[2]
        duration -= 1
#        print "t-1: " + repr(duration) + " s"
        deb._orbit.find(z, v, szeta, czeta, sgamma, cgamma)
#        print "new orb found"
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
#            print "Repeat"
            deb.step()
            self.fire(deb, duration)
    
    def fluence(self, z, Teff):
        return self._W*self._Deff*4*Teff / (math.pi*math.pow(self._M2*self._a*self._laser._lambda, 2)*math.pow(z, 2))

    def spot(self, z):
        return self._a*self._M2*self._laser._lambda*z / self._Deff
    
    def __del__(self):
        print "Beam terminated"
