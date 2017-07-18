#!/usr/bin/python

import math
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
        self.update()

    def update(self):
        self._r = self.__orbit.a*(1- math.pow(self.__orbit.ep, 2))/(1+self.__orbit.ep*math.cos(self._nu))
        self._v = math.sqrt(consts.mu*(2/self._r - 1/self.__orbit.a))
        self.v0 = math.sqrt(consts.mu*(2/self.__orbit.rp - 1/self.__orbit.a))
        self._theta = math.asin(self.__orbit.rp*self.v0/(self._r*self._v))
        if self._nu < math.pi:
            self._theta = math.pi - self._theta
        # print "alpha: " + repr(self._theta*180/math.pi)

    def measure(self):
        return{'r':self._r, 'v':self._v, 'theta':self._theta, 'nuw':self.__orbit.omega+self._nu}

    def plot(self, line):
        self.__orbit.plot(line)
        plt.hold('on')
        plt.plot(self._r*math.cos(self.__orbit.omega+self._nu), self._r*math.sin(self.__orbit.omega+self._nu), 'o' )
        #plt.show()

    def hit(self, beam):
        

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

        
