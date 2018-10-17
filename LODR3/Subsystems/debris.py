#!/usr/bin/python

import math
from .orbit import orbit as Orbit
from .Support_Files import constants as consts
from .Support_Files import extmath
import matplotlib.pyplot as plt
import numpy as np


class debris:
    def __init__(self, ID, etac, Cm, size, mass, nu, orbit=None, rp=None, ep=None, omega=None):
        self.ID = ID
        self.compute(etac, Cm, size, mass, nu, orbit, rp, ep, omega)

    def compute(self, etac, Cm, size, mass, nu, orbit=None, rp=None, ep=None, omega=None):
        self.__Transfer = np.empty(shape=(0,2))
        self._Cm = Cm
        self._orbit = orbit
        self._size = size
        self._mass = mass
#        self._orientation = orientation
        if orbit != None:
            self._orbit = orbit
        else:
            self._orbit = Orbit()
            self._orbit.make(rp, ep, omega)
        self._nu = nu
        self._etac = etac
        self._snu = math.sin(self._nu)
        self._cnu = math.cos(self._nu)
        self._r = self._orbit.a*(1- math.pow(self._orbit.ep, 2))/(1+self._orbit.ep*self._cnu)
        self._v = math.sqrt(consts.mu*(2/self._r - 1/self._orbit.a))*1.0
        self._sgamma = self._orbit.rp*self._orbit.vp / (self._r*self._v)
        self._cgamma = math.sqrt(1 - math.pow(self._sgamma, 2))
        if self._nu < math.pi:
            self._cgamma = - self._cgamma

    def step(self):
        dnu = self._orbit.a*self._orbit.b*self._orbit.n / math.pow(self._r, 2)
        vp = self._orbit.vp #math.sqrt(consts.mu*(2/self._orbit.rp - 1/self._orbit.a))
        self._nu = self._nu + dnu
        if self._nu > 2*math.pi:
            self._nu -= 2*math.pi
        elif self._nu < 0:
            self._nu += 2*math.pi
        self._snu = math.sin(self._nu)
        self._cnu = math.cos(self._nu)
        self._r = self._orbit.a*(1- math.pow(self._orbit.ep, 2))/(1+self._orbit.ep*self._cnu)
        self._v = math.sqrt(consts.mu*(2/self._r - 1/self._orbit.a))*1.0
        self._sgamma = self._orbit.rp*vp / (self._r*self._v)
        if self._sgamma > 1:
            print("Sin gamma = " + repr(self._sgamma))
            print("vp = " + repr(self.vp) + "  v = " + repr(self._v))
            print("rp = " + repr(self._orbit.rp) + "  r = " + repr(self._r))
        self._cgamma = math.sqrt(1 - math.pow(self._sgamma, 2))
        if self._nu < math.pi:
            self._cgamma = - self._cgamma

    def measure(self):
        snuw = extmath.sinplus(self._orbit.sw, self._orbit.cw, self._snu, self._cnu)
        cnuw = extmath.cosplus(self._orbit.sw, self._orbit.cw, self._snu, self._cnu)
        cphi = extmath.cosminus(snuw, cnuw, consts.slat, consts.clat) 
        sphi = extmath.sinminus(snuw, cnuw, consts.slat, consts.clat) 
        z = math.sqrt(math.pow(consts.Re, 2) + math.pow(self._r, 2) - 2*consts.Re*self._r*cphi)
        cdelta = (math.pow(self._r, 2) + math.pow(z, 2) - math.pow(consts.Re, 2)) / (2*self._r*z)
        sdelta = consts.Re/z*sphi
        calpha = (math.pow(consts.Re, 2) + math.pow(z, 2) - math.pow(self._r, 2)) / (2*consts.Re*z)
        salpha = self._r/z*(-sphi)
        cbeta = extmath.cosminus(salpha, calpha, 1, 0) # alpha - pi/2
        sbeta = extmath.sinminus(salpha, calpha, 1, 0) # alpha - pi/2
        szeta = extmath.sinminus(self._sgamma, self._cgamma, sdelta, cdelta)
        czeta = extmath.cosminus(self._sgamma, self._cgamma, sdelta, cdelta)
        return{'z':z, 'v':self._v, 'szeta':szeta, 'czeta':czeta,
                'sbeta':sbeta, 'cbeta':cbeta, 'sdelta':sdelta,
                'cdelta':cdelta, 'sphi':sphi, 'cphi':cphi}

    def get_beta(self):
        snuw = extmath.sinplus(self._orbit.sw, self._orbit.cw, self._snu, self._cnu)
        cnuw = extmath.cosplus(self._orbit.sw, self._orbit.cw, self._snu, self._cnu)
        cphi = extmath.cosminus(snuw, cnuw, consts.slat, consts.clat) 
        sphi = extmath.sinminus(snuw, cnuw, consts.slat, consts.clat) 
        z = math.sqrt(math.pow(consts.Re, 2) + math.pow(self._r, 2) - 2*consts.Re*self._r*cphi)
        calpha = (math.pow(consts.Re, 2) + math.pow(z, 2) - math.pow(self._r, 2)) / (2*consts.Re*z)
        salpha = self._r/z*(-sphi)
        cbeta = extmath.cosminus(salpha, calpha, 1, 0) # alpha - pi/2
        sbeta = extmath.sinminus(salpha, calpha, 1, 0) # alpha - pi/2
        return math.atan2(sbeta, cbeta)



#    def plot(self, line):
#        self._orbit.plot(line)
#        plt.hold('on')
#        plt.plot(self._r*extmath.cosplus(self._orbit.sw, self._orbit.cw, self._snu, self._cnu), self._r*extmath.sinplus(self._orbit.sw, self._orbit.cw, self._snu, self._cnu), 'o' )

    def plot_data(self):
        X = self._r*extmath.cosplus(self._orbit.sw, self._orbit.cw, self._snu, self._cnu)
        Y = self._r*extmath.sinplus(self._orbit.sw, self._orbit.cw, self._snu, self._cnu)
        return [X, Y]

    def hit(self, ds, Phi, szeta, czeta, reps):
        if ds > 2*self._size:
            u = math.pow(ds/(2*self._size), 2) 
        else:
            u = 1
        print("u: " + str(u))
        dvz = reps*self._etac*self._Cm*Phi / (self._mass*u/(math.pi*math.pow(self._size, 2)))
#        dvz = reps*self._etac*self._Cm*Phi / (self._mass/(math.pi*math.pow(self._size, 2)))
        print("dvz: " + str(dvz))
        print("v1: " + str(self._v))
        v = math.sqrt(math.pow((self._v - dvz*czeta), 2) + math.pow((dvz*szeta), 2))
        sdzeta = dvz*szeta/v
        cdzeta = (self._v - dvz*czeta) / v
        self._v = v*1.0
        print("v2: " + str(self._v))
        szeta2 = extmath.sinplus(szeta, czeta, sdzeta, cdzeta)
        czeta2 = extmath.cosplus(szeta, czeta, sdzeta, cdzeta)
        return np.array([szeta2, czeta2, v])

    def transfer(self):
#        print("Transfer")
        self.__Transfer = np.vstack((self.__Transfer, self.plot_data()))

    def transfer_data(self):
#        print(len(self.__Transfer))
        self.transfer()
#        print(len(self.__Transfer))
        Temp = self.__Transfer
        self.__Transfer = np.empty(shape=(0,2))
        return Temp

