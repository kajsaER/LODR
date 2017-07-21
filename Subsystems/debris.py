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
        self._snu = math.sin(self._nu)
        self._cnu = math.cos(self._nu)
        self.update()

    def update(self):
        self._r = self.__orbit.a*(1- math.pow(self.__orbit.ep, 2))/(1+self.__orbit.ep*self._cnu)
        cnuw = extmath.cosplus(self._snu, self._cnu, self.__orbit.sw, self.__orbit.cw) 
        snuw = extmath.sinplus(self._snu, self._cnu, self.__orbit.sw, self.__orbit.cw) 
        cphi = extmath.cosminus(consts.slat, consts.clat, snuw, cnuw) 
        sphi = extmath.sinminus(consts.slat, consts.clat, snuw, cnuw) 
        self._v = math.sqrt(consts.mu*(2/self._r - 1/self.__orbit.a))
        self.v0 = math.sqrt(consts.mu*(2/self.__orbit.rp - 1/self.__orbit.a))
        self._theta = math.asin(self.__orbit.rp*self.v0/(self._r*self._v))
        if self._nu < math.pi:
            self._theta = math.pi - self._theta
        self._stheta = math.sin(self._theta)
        self._ctheta = math.cos(self._theta)
        # print "alpha: " + repr(self._theta*180/math.pi)

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
        return{'z':z, 'v':self._v, 'szeta':szeta, 'czeta':czeta, 'sgamma':sgamma, 'cgamma':cgamma}

    def plot(self, line):
        self.__orbit.plot(line)
        plt.hold('on')
        plt.plot(self._r*math.cos(self.__orbit.omega+self._nu), self._r*math.sin(self.__orbit.omega+self._nu), 'o' )
        #plt.show()

#    def hit(self, beam):
#        z = 

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

        
