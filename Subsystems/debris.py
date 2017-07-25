#!/usr/bin/python

import math
import extmath
import matplotlib.pyplot as plt
import constants as consts

class debris:
    def __init__(self, shape, Cm, size, mass, orientation, orbit, nu):
        self._shape = shape
        self._Cm = Cm
        self._size = size
        self._mass = mass
        self._orientation = orientation
        self.__orbit = orbit
        self._nu = nu
        self._etac = 0.3
        self._snu = math.sin(self._nu)
        self._cnu = math.cos(self._nu)
        self.v0 = math.sqrt(consts.mu*(2/self.__orbit.rp - 1/self.__orbit.a))
        self._r = self.__orbit.a*(1- math.pow(self.__orbit.ep, 2))/(1+self.__orbit.ep*self._cnu)
        self._v = math.sqrt(consts.mu*(2/self._r - 1/self.__orbit.a))
        self._stheta = self.__orbit.rp*self.v0 / (self._r*self._v)
        self._ctheta = math.sqrt(1 - math.pow(self._stheta, 2))
        if self._nu < math.pi:
            self._ctheta = - self._ctheta

    def step(self):
        dnu = self.__orbit.a*self.__orbit.b*self.__orbit.n / math.pow(self._r, 2)
        self._nu = self._nu + dnu
        if self._nu > 2*math.pi:
            self._nu -= 2*math.pi
        self._snu = math.sin(self._nu)
        self._cnu = math.cos(self._nu)
        self._r = self.__orbit.a*(1- math.pow(self.__orbit.ep, 2))/(1+self.__orbit.ep*self._cnu)
        self._v = math.sqrt(consts.mu*(2/self._r - 1/self.__orbit.a))
        self._stheta = self.__orbit.rp*self.v0 / (self._r*self._v)
        self._ctheta = math.sqrt(1 - math.pow(self._stheta, 2))
        if self._nu < math.pi:
            self._ctheta = - self._ctheta

    def measure(self):
        snuw = extmath.sinplus(self.__orbit.sw, self.__orbit.cw, self._snu, self._cnu)
        cnuw = extmath.cosplus(self.__orbit.sw, self.__orbit.cw, self._snu, self._cnu)
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
        self.__orbit.plot(line)
        plt.hold('on')
        plt.plot(self._r*math.cos(self.__orbit.omega+self._nu), self._r*math.sin(self.__orbit.omega+self._nu), 'o' )
        #plt.show()

    def hit(self, beam):
        meas = self.measure()
        z = meas['z']
        szeta = meas['szeta']
        czeta = meas['czeta']
        sgamma = meas['sgamma']
        cgamma = meas['cgamma']
        sdelta = meas['sdelta']
        cdelta = meas['cdelta']
        sphi = meas['sphi']
        cphi = meas['cphi']
        Phi = beam.fluence(z, 0.5)
        ds = beam.spot(z)
        if ds >= self._size:
            dvz = self._etac*self._Cm*Phi / (self._mass/(math.pi*math.pow(self._size, 2)))
            v = math.sqrt(math.pow((self._v - dvz*czeta), 2) + math.pow((dvz*szeta), 2))
            sdzeta = dvz*szeta/v
            cdzeta = (self._v - dvz*czeta) / v
            self._v = v
            szeta = extmath.sinplus(szeta, czeta, sdzeta, cdzeta)
            czeta = extmath.cosplus(szeta, czeta, sdzeta, cdzeta)
            self.__orbit.find(z, self._v, szeta, czeta, sgamma, cgamma)
            sw = self.__orbit.sw
            cw = self.__orbit.cw
            spw = extmath.sinplus(sphi, cphi, sw, cw)
            cpw = extmath.cosplus(sphi, cphi, sw, cw)
            self._snu = extmath.sinminus(consts.slat, consts.clat, spw, cpw)
            self._cnu = extmath.cosminus(consts.slat, consts.clat, spw, cpw)
            self._nu = math.atan2(self._snu, self._cnu)
            if self._nu < 0:
                self._nu += 2*math.pi

            self._stheta = extmath.sinplus(sdelta, cdelta, szeta, czeta)
            self._ctheta = extmath.cosplus(sdelta, cdelta, szeta, czeta)
        else:
            print "Spot size too small."


    def __del__(self):
        print "Debris deleted"



#class shape:
#   def __init__(self, form, size):
#       self._type = form
#       if form == ball:
#           self._radious = size
#       elif form == square:
#           self._side = size
#
#   def __del__(self):
#       print "No shape"

        
