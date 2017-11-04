#!/usr/bin/python

import math
import extmath
import matplotlib.pyplot as plt
import constants as consts
import numpy as np

class debris:
    def __init__(self, shape, Cm, size, mass, orientation, orbit, nu):
        self._shape = shape
        self._Cm = Cm
        self._size = size
        self._mass = mass
        self._orientation = orientation
        self._orbit = orbit
        self._nu = nu
        self._etac = 0.3
        self._snu = math.sin(self._nu)
        self._cnu = math.cos(self._nu)
        self.v0 = math.sqrt(consts.mu*(2/self._orbit.rp - 1/self._orbit.a))
        self._r = self._orbit.a*(1- math.pow(self._orbit.ep, 2))/(1+self._orbit.ep*self._cnu)
        self._v = math.sqrt(consts.mu*(2/self._r - 1/self._orbit.a))
        self._stheta = self._orbit.rp*self.v0 / (self._r*self._v)
        self._ctheta = math.sqrt(1 - math.pow(self._stheta, 2))
        if self._nu < math.pi:
            self._ctheta = - self._ctheta

    def step(self):
        dnu = self._orbit.a*self._orbit.b*self._orbit.n / math.pow(self._r, 2)
#       self.v0 = math.sqrt(consts.mu*(2/self._orbit.rp - 1/self._orbit.a))
        self._nu = self._nu + dnu
        if self._nu > 2*math.pi:
            self._nu -= 2*math.pi
        elif self._nu < 0:
            self._nu += 2*math.pi
        self._snu = math.sin(self._nu)
        self._cnu = math.cos(self._nu)
        self._r = self._orbit.a*(1- math.pow(self._orbit.ep, 2))/(1+self._orbit.ep*self._cnu)
        self._v = math.sqrt(consts.mu*(2/self._r - 1/self._orbit.a))
        self._stheta = self._orbit.rp*self.v0 / (self._r*self._v)
        if self._stheta > 1:
            print "Sin Theta = " + repr(self._stheta)
        self._ctheta = math.sqrt(1 - math.pow(self._stheta, 2))
        if self._nu < math.pi:
            self._ctheta = - self._ctheta

    def measure(self):
        snuw = extmath.sinplus(self._orbit.sw, self._orbit.cw, self._snu, self._cnu)
        cnuw = extmath.cosplus(self._orbit.sw, self._orbit.cw, self._snu, self._cnu)
        cphi = extmath.cosminus(consts.slat, consts.clat, snuw, cnuw) 
        sphi = extmath.sinminus(consts.slat, consts.clat, snuw, cnuw) 
        z = math.sqrt(math.pow(consts.Re, 2) + math.pow(self._r, 2) - 2*consts.Re*self._r*cphi)
        cdelta = (math.pow(self._r, 2) + math.pow(z, 2) - math.pow(consts.Re, 2)) / (2*self._r*z)
        sdelta = consts.Re/z*sphi
        calpha = (math.pow(consts.Re, 2) + math.pow(z, 2) - math.pow(self._r, 2)) / (2*consts.Re*z)
        salpha = self._r/z*sphi
        cgamma = extmath.cosminus(salpha, calpha, 1, 0) # alpha - pi/2
        sgamma = extmath.sinminus(salpha, calpha, 1, 0) # alpha - pi/2
        szeta = extmath.sinminus(self._stheta, self._ctheta, sdelta, cdelta)
        czeta = extmath.cosminus(self._stheta, self._ctheta, sdelta, cdelta)
        return{'z':z, 'v':self._v, 'szeta':szeta, 'czeta':czeta, 'sgamma':sgamma, 'cgamma':cgamma, 'sdelta':sdelta,
                'cdelta':cdelta, 'sphi':sphi, 'cphi':cphi}

    def plot(self, line):
        self._orbit.plot(line)
        plt.hold('on')
        plt.plot(self._r*extmath.cosplus(self._orbit.sw, self._orbit.cw, self._snu, self._cnu), self._r*extmath.sinplus(self._orbit.sw, self._orbit.cw, self._snu, self._cnu), 'o' )

    def hit(self, ds, Phi, szeta, czeta, reps):
#       if ds > self._size:
#           u = math.pow(ds/(2*self._size), 2) 
#       else:
#           u = 1
#       dvz = reps*self._etac*self._Cm*Phi / (self._mass*u/(math.pi*math.pow(self._size, 2)))
        dvz = reps*self._etac*self._Cm*Phi / (self._mass/(math.pi*math.pow(self._size, 2)))
        v = math.sqrt(math.pow((self._v - dvz*czeta), 2) + math.pow((dvz*szeta), 2))
        sdzeta = dvz*szeta/v
        cdzeta = (self._v - dvz*czeta) / v
        self._v = v
        szeta2 = extmath.sinplus(szeta, czeta, sdzeta, cdzeta)
        czeta2 = extmath.cosplus(szeta, czeta, sdzeta, cdzeta)
        return np.array([szeta2, czeta2, v])

    def __del__(self):
        print "Debris deleted"
