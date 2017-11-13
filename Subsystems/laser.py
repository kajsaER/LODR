#!/usr/bin/python

import math
import extmath
import constants as consts
import numpy as np

NAN = float('nan')

class laser:

    def __init__(self):
        self._P = NAN                   # The power of the chosen laser
        self._W =  NAN                  # Pulse energy          self._P/self._frep
        self._lambda = NAN              # The wavelength of the chosen laser
        self._M2 = NAN                  # The beam quality factor of the chosen laser
        self._Cb = NAN                  # Beam coefficient
        self._frep = NAN                # Repetition rate
        self._tau = NAN                 # Pulse duration
        self._dubf = False              # Bool for indication of frequency doubling

    def switch(self, LaserType):
        self._P = extmath.myfloat(LaserType.get('power'))
        self._W = extmath.myfloat(LaserType.get('energy'))
        self._lambda = extmath.myfloat(LaserType.get('lambda'))
        self._M2 = extmath.myfloat(LaserType.get('m2'))
        self._Cb = extmath.myfloat(LaserType.get('cb'))
        self._frep = extmath.myfloat(LaserType.get('repetition rate'))
        self._tau = extmath.myfloat(LaserType.get('pulse duration'))
        self._dubf = False

    def doubfreq(self):
        self._dubf = True
        self._lambda = self._lambda/2

    def normfreq(self):
        self._dubf = False
        self._lambda = self._lambda*2

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
            debval = deb.hit(self.spot(z, ant.Deff(), atm),
                    self.fluence(z, ant.Deff(), atm), szeta,
                    czeta, self._frep*duration)
            szeta = debval[0]
            czeta = debval[1]
            v = debval[2]
        else :
            debval = deb.hit(self.spot(z, ant.Deff(), atm),
                    self.fluence(z,ant.Deff(), atm), szeta,
                    czeta, self._frep)
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

