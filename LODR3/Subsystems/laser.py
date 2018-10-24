#!/usr/bin/python

import math
from .Support_Files import constants as consts
from .Support_Files import extmath
import numpy as np

NAN = float('nan')      # Define NAN as a float variable with value nan

class laser:

    def __init__(self):
        self._P = NAN               # The power of the chosen laser
        self._W =  NAN              # Pulse energy
        self._lambda = NAN          # The wavelength of the chosen laser
        self._M2 = NAN              # The beam quality factor of the chosen laser
        self._Cd = NAN              # Beam coefficient
        self._frep = NAN            # Repetition rate
        self._tau = NAN             # Pulse duration
        self._dubf = False          # Bool for indication of frequency doubling

    def switch(self, LaserType):    # Set values according to chosen laser
        self._P = extmath.myfloat(LaserType.get('power'))
        self._W = extmath.myfloat(LaserType.get('energy'))
        self._lambda = extmath.myfloat(LaserType.get('lambda'))
        self._M2 = extmath.myfloat(LaserType.get('m2'))
        self._Cd = extmath.myfloat(LaserType.get('cd'))
        self._frep = extmath.myfloat(LaserType.get('repetition rate'))
        self._tau = extmath.myfloat(LaserType.get('pulse duration'))
        self._dubf = False

    def doubfreq(self):             # Make the frequency double the value
        self._dubf = True
        self._lambda = self._lambda/2

    def normfreq(self):             # Reset to normal value
        self._dubf = False
        self._lambda = self._lambda*2

    def spot(self, z, Deff, atm):   # Calculate and return the spot size (ds) at distance z
        diveff = self.div(Deff, atm)# Get the effective divergence angle
        return 2 * diveff * z
    
    def fluence(self, z, Deff, atm):# Calculate and return the fluence (Φ) at distance z
        diveff = self.div(Deff, atm)# Get the effective divergence angle θeff
        return self._W*atm.Teff() / (math.pi*math.pow(diveff, 2)*math.pow(z, 2))

    def div(self, Deff, atm):       # Calculate and return the effective divergence angle
        divM2 = self._M2 * self._Cd/4 * self._lambda/(Deff/2)   # M² divergence angle
        return math.sqrt(math.pow(divM2, 2) + atm.divergence2(self._lambda))

    def fire(self, ant, deb, duration, atm, beta_min, beta_max, zeta_min, zeta_max):
        deb.transfer()              # Store starting coordinates
        meas = deb.measure()        # Measure the relevant variables available at Gs
        z = meas['z']               # Distance z
        szeta = meas['szeta']       # ∠vz
        czeta = meas['czeta']
        sbeta = meas['sbeta']       # Elevation angle
        cbeta = meas['cbeta']
        sdelta = meas['sdelta']     # ∠zr
        cdelta = meas['cdelta']
        sphi = meas['sphi']         # ∠rRe
        cphi = meas['cphi']
        print("FRIE! tau: " + repr(duration))
        if duration <= 1:           # If the duration is less than 1s, calculate for it all
            debval = deb.hit(self.fluence(z, ant.Deff(), atm), szeta,
                    czeta, self._frep*duration)     # Get new velocity after hit by laser
            szeta = debval[0]       # New ∠vz
            czeta = debval[1]
            v = debval [2]          # New velocity
            deb._orbit.find(z, v, szeta, czeta, sbeta, cbeta)   # Find orbit fitting new values
            deb.update_nu()
#            deb._sgamma = extmath.sinplus(sdelta, cdelta, szeta, czeta) # γ = δ + ζ
#            deb._cgamma = extmath.cosplus(sdelta, cdelta, szeta, czeta) # ∠vr
        else :                      # If the duration is more than 1s, calculate for 1s
            debval = deb.hit(self.fluence(z,ant.Deff(), atm), szeta,
                    czeta, self._frep)
            szeta = debval[0]           # New ∠vz
            czeta = debval[1]
            v = debval[2]               # New velocity
            duration -= 1               # Decreas duration with 1s
            deb.move()
            meas = deb.measure()    # Measure again
            beta = math.atan2(meas['sbeta'], meas['cbeta']) # Elevation angle
            zeta = math.atan2(meas['szeta'], meas['cbeta']) # ∠vz
            if (beta_min < beta < beta_max) and (zeta_min < zeta < zeta_max):   # If still in range
                self.fire(ant, deb, duration, atm, beta_min, beta_max, 
                          zeta_min, zeta_max)  # Fire again
#        deb._orbit.find(z, v, szeta, czeta, sbeta, cbeta)   # Find orbit fitting new values
#        sw = deb._orbit.sw          # New argument of perigee
#        cw = deb._orbit.cw
#        spp = extmath.sinplus(sphi, cphi, consts.slat, consts.clat) # φ + ∅
#        cpp = extmath.cosplus(sphi, cphi, consts.slat, consts.clat)
#        deb._snu = extmath.sinminus(spp, cpp, sw, cw)               # ν = φ + ∅ - ω
#        deb._cnu = extmath.cosminus(spp, cpp, sw, cw)
#        deb._nu = math.atan2(deb._snu, deb._cnu)
#        if deb._nu < 0:             # Make ν ∈ [0, 2π)
#            deb._nu += 2*math.pi
#        deb._sgamma = extmath.sinplus(sdelta, cdelta, szeta, czeta) # γ = δ + ζ
#        deb._cgamma = extmath.cosplus(sdelta, cdelta, szeta, czeta) # ∠vr
#        if duration > 0:            # If there is still time left in duration
#            deb.step()              # Let debris move along its new orbit, one step
#            meas = deb.measure()    # Measure again
#            beta = math.atan2(meas['sbeta'], meas['cbeta']) # Elevation angle
#            zeta = math.atan2(meas['szeta'], meas['cbeta']) # ∠vz
#            if (beta_min < beta < beta_max) and (zeta_min < zeta < zeta_max):   # If still in range
#                self.fire(ant, deb, duration, atm, beta_min, beta_max, 
#                          zeta_min, zeta_max)  # Fire again

    def get_data(self):             # Get variable values
        string = ("P: " + str(self._P) + "\n" +
                  "Cd: " + str(self._Cd) + "\n" +
                  "W: " + str(self._W) + "\n" +
                  "lam: " + str(self._lambda) + "\n" +
                  "M2: " + str(self._M2) + "\n" +
                  "frep: " + str(self._frep) + "\n" +
                  "tau: " + str(self._tau) + "\n" +
                  "dub: " + str(self._dubf) + "\n")
        return string
