#!/usr/bin/python

import math
from .Support_Files import constants as consts
from .Support_Files import extmath
#from . import Support_Files.constants as consts
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
        self._Cb = extmath.myfloat(LaserType.get('cd'))
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

    def fire(self, ant, deb, duration, atm, beta_min, beta_max, zeta_min, zeta_max):
        deb.transfer()
        meas = deb.measure()
        z = meas['z']
        szeta = meas['szeta']
        czeta = meas['czeta']
        sbeta = meas['sbeta']
        cbeta = meas['cbeta']
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
        deb._orbit.find(z, v, szeta, czeta, sbeta, cbeta)
        sw = deb._orbit.sw
        cw = deb._orbit.cw
        spw = extmath.sinplus(sphi, cphi, sw, cw)
        cpw = extmath.cosplus(sphi, cphi, sw, cw)
        deb._snu = extmath.sinminus(consts.slat, consts.clat, spw, cpw)
        deb._cnu = extmath.cosminus(consts.slat, consts.clat, spw, cpw)
        deb._nu = math.atan2(deb._snu, deb._cnu)
        if deb._nu < 0:
            deb._nu += 2*math.pi
        deb._sgamma = extmath.sinplus(sdelta, cdelta, szeta, czeta)
        deb._cgamma = extmath.cosplus(sdelta, cdelta, szeta, czeta)
        if duration > 0:
#            deb.transfer()
            deb.step()
            meas = deb.measure()
            beta = math.atan2(meas['sbeta'], meas['cbeta'])
            zeta = math.atan2(meas['szeta'], meas['cbeta'])
#            print("beta: " + str(beta) + "    zeta: " + str(zeta))
            if (beta_min < beta < beta_max) and (zeta_min < zeta < zeta_max):
#                print("Fire again")
                self.fire(ant, deb, duration, atm, beta_min, beta_max, zeta_min, zeta_max)

    def Print(self):
        print("P: " + str(self._P))                   # The power of the chosen laser
        print("Cb: " + str(self._Cb))                 # Beam coefficient
        print("W: " + str(self._W))                   # Pulse energy          self._P/self._frep
        print("lam: " + str(self._lambda))            # The wavelength of the chosen laser
        print("M2: " + str(self._M2))                 # The beam quality factor of the chosen laser
        print("frep: " + str(self._frep))             # Repetition rate
        print("tau: " + str(self._tau))               # Pulse duration
        print("dub: " + str(self._dubf))              # Bool for indication of frequency doubling

#    def __del__(self):
#        print "Laser has been deleted"

