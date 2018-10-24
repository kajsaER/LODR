#!/usr/bin/python

import math
from .orbit import orbit as Orbit
from .Support_Files import constants as consts
from .Support_Files import extmath
import matplotlib.pyplot as plt
import numpy as np

tol = 1e-4      # Tolerance for 0

class debris:
    def __init__(self, ID, etac, Cm, size, mass, nu,
                 orbit=None, rp=None, ep=None, omega=None):
        self.ID = ID        # Identifier for the specific piece of debris
        self.compute(etac, Cm, size, mass, nu, orbit, rp, ep, omega)

    def compute(self, etac, Cm, size, mass, nu,     # Calculate and set 
                orbit=None, rp=None, ep=None, omega=None):  # all variables
        self.__Transfer = np.empty(shape=(0,2))     # Empty matrix for transfer
        self._Cm = Cm           # Momentum coupling coefficient
        self._orbit = orbit     # Orbit
        self._size = size       # Debris diameter in m
        self._mass = mass       # Debris mass in kg
#        self._orientation = orientation   # Not used for assumed spherical debris
        if orbit != None:       # If an orbit was provided, use it
            self._orbit = orbit
            omega = orbit.omega
        else:                   # If no orbit was provided, make one
            self._orbit = Orbit()
            self._orbit.make(rp, ep, omega)
        self._nu = nu           # True anomaly
        self._etac = etac       # Combined coefficiency factor
        self._snu = math.sin(self._nu)
        self._cnu = math.cos(self._nu)
        self._r = (self._orbit.a*(1- math.pow(self._orbit.ep, 2)) / 
                   (1+self._orbit.ep*self._cnu))    # Orbital radius
        self._v = math.sqrt(consts.mu*(2/self._r - 1/self._orbit.a))*1.0    # Velocity
        self._sgamma = self._orbit.rp*self._orbit.vp / (self._r*self._v)    # ∠rv
        self._cgamma = math.sqrt(1 - math.pow(self._sgamma, 2))     # cos(γ) ≥ 0
        if self._nu < math.pi:      # If ν < π then cos(γ) < 0
            self._cgamma = - self._cgamma
        self.__omicron = (omega + nu) % (2*math.pi)

    def step(self):                 # Take a step along the orbit
        dnu = (self._orbit.a*self._orbit.b*self._orbit.n /  # Δν = a*b*n/r²
               math.pow(self._r, 2))
        vp = self._orbit.vp         # Velocity at perigee
        self._nu = (self._nu + dnu) % (2*math.pi)   # ν ∈ [0, 2π)
        self._snu = math.sin(self._nu)
        self._cnu = math.cos(self._nu)
        self._r = (self._orbit.a*(1- math.pow(self._orbit.ep, 2)) / 
                   (1+self._orbit.ep*self._cnu))    # r = a(1-ε²)/(1-ε cos(ν))
        self._v = math.sqrt(consts.mu*(2/self._r - 1/self._orbit.a))*1.0    #Vis-viva
        self._sgamma = self._orbit.rp*vp / (self._r*self._v)    # Law of Sines
        self.__omicron = (self.__omicron + dnu) % (2*math.pi) 

        if self._sgamma > 1:        # Impossible γ causes exception
            raise Exception("Sin gamma = " + repr(self._sgamma) + ".\n" +
                            "vp = " + repr(self.vp) + "  v = " + repr(self._v) + ".\n" +
                            "rp = " + repr(self._orbit.rp) + "  r = " + repr(self._r))
        
        self._cgamma = math.sqrt(1 - math.pow(self._sgamma, 2)) # Pythagorean trigonometric identity
        
        if self._nu < math.pi:      # If ν < π then γ ∈ [π/2, 3π/2]
            self._cgamma = - self._cgamma

    def measure(self):          # Calculate and return values as measured from Gs
        so = math.sin(self.__omicron)       # ο = ν + ω
        co = math.cos(self.__omicron)
        cphi = extmath.cosminus(so, co, consts.slat, consts.clat)   # φ = ν + ω - ∅
        sphi = extmath.sinminus(so, co, consts.slat, consts.clat) 
        z = math.sqrt(math.pow(consts.Re, 2) + math.pow(self._r, 2)
                      - 2*consts.Re*self._r*cphi)       # Law of Cosines
        cdelta = (math.pow(self._r, 2) + math.pow(z, 2) - math.pow(consts.Re, 2)) / (2*self._r*z)
        sdelta = consts.Re/z*(-sphi)                    # Law of Sines
        cxi = (math.pow(consts.Re, 2) + math.pow(z, 2) - math.pow(self._r, 2)) / (2*consts.Re*z)
        sxi = self._r/z*(-sphi)
        cbeta = extmath.cosminus(sxi, cxi, 1, 0)  # β = α - π/2
        sbeta = extmath.sinminus(sxi, cxi, 1, 0)
        szeta = extmath.sinminus(self._sgamma, self._cgamma, sdelta, cdelta)    # ζ = γ - δ
        czeta = extmath.cosminus(self._sgamma, self._cgamma, sdelta, cdelta)
        print("Measure")
        print("r: " + repr(self._r) + "   v: " + repr(self._v) + "   gamma: " + repr(math.degrees(math.atan2(self._sgamma, self._cgamma))))
        return{'z':z, 'v':self._v, 'szeta':szeta, 'czeta':czeta,
                'sbeta':sbeta, 'cbeta':cbeta, 'sdelta':sdelta,
                'cdelta':cdelta, 'sphi':sphi, 'cphi':cphi}

    def get_beta(self):         # Calculate and return the elevation angle
        so = math.sin(self.__omicron)
        co = math.cos(self.__omicron)
        cphi = extmath.cosminus(so, co, consts.slat, consts.clat) 
        sphi = extmath.sinminus(so, co, consts.slat, consts.clat) 
        z = math.sqrt(math.pow(consts.Re, 2) + math.pow(self._r, 2) - 2*consts.Re*self._r*cphi)
        cxi = (math.pow(consts.Re, 2) + math.pow(z, 2) - math.pow(self._r, 2)) / (2*consts.Re*z)
        sxi = self._r/z*(-sphi)
        cbeta = extmath.cosminus(sxi, cxi, 1, 0)  # β = α - π/2
        sbeta = extmath.sinminus(sxi, cxi, 1, 0)
        return math.atan2(sbeta, cbeta)

    def plot_data(self):        # Calculate and return [x,y] coordinates
        X = self._r*math.cos(self.__omicron)
        Y = self._r*math.sin(self.__omicron)
        return [X, Y]

    def hit(self, Phi, szeta, czeta, reps): # Calculate and return v and ζ after hit by laser
        dvz = (reps*self._etac*self._Cm*Phi /       # velocity change in z direction
               (self._mass/(math.pi*math.pow((self._size/2), 2))))
        v = math.sqrt(math.pow((self._v - dvz*czeta), 2) + math.pow((dvz*szeta), 2))    # New velocity
        sdzeta = dvz*szeta/v                # Sin(Δζ)
        cdzeta = (self._v - dvz*czeta) / v  # Cos(Δζ)
        self._v = v*1.0
        szeta2 = extmath.sinplus(szeta, czeta, sdzeta, cdzeta)  # ζ₂ = ζ₁ + Δζ
        czeta2 = extmath.cosplus(szeta, czeta, sdzeta, cdzeta)
        sgamma = self._sgamma
        cgamma = self._cgamma
        self._sgamma = extmath.sinplus(sgamma, cgamma, sdzeta, cdzeta)
        self._cgamma = extmath.cosplus(sgamma, cgamma, sdzeta, cdzeta)
        print("Hit")
        print("r: " + repr(self._r) + "   v: " + repr(v) + "   gamma: " + repr(math.degrees(math.atan2(sgamma, cgamma))))
        return np.array([szeta2, czeta2, v])

    def update_nu(self):    # Update ν to match ο and ω
        self._nu = (self.__omicron - self._orbit.omega) % (2*math.pi)
        self._snu = math.sin(self._nu)
        self._cnu = math.cos(self._nu)

    def move(self):
        print("In Move")
        dt = 1.0            # Time step is 1s
        r1 = self._r        # Starting values
        v1 = self._v
        sgamma1 = self._sgamma
        cgamma1 = self._cgamma
        r2 = math.sqrt(math.pow(r1, 2) + math.pow(v1*dt, 2) - 2*r1*v1*dt*cgamma1)   # r₂ = √(r₁² + (v₁*dt)² - 2*r₁*v₁*dt*cos(γ₁))
        sdo = sgamma1 / r2 * v1*dt      # sin(Δο) = sin(γ₁) / r₂ * v₁*dt
        cdo = ((math.pow(r1, 2) + math.pow(r2, 2) - math.pow(v1*dt, 2)) /   # (r₁² + r₂² - (v₁*dt)²) /
                (2 * r1 * r2))                                              #     (2 * r₁ * r₂)
        do = math.atan2(sdo, cdo)
        self.__omicron = (self.__omicron + do) % (2*math.pi)    # ο₂ = ο₁ + Δο ∈ [0, 2π)

        v2 = math.sqrt(2*(consts.mu/r2 - consts.mu/r1) + math.pow(v1, 2))   # Constant energy and mass
        sgamma2 = (r1*v1) / (r2*v2) * sgamma1                               # Constant angular momentum
        cgamma2 = math.sqrt(1 - math.pow(sgamma2, 2))                       # Pythagorean trigonometric identity

        self._r = r2        # Store new values
        self._v = v2
        self._sgamma = sgamma2
        self._cgamma = cgamma2

        print("r1: " + repr(r1) + "   v1: " + repr(v1) + "   gamma1: " + repr(math.degrees(math.atan2(sgamma1, cgamma1))))
        print("r2: " + repr(r2) + "   v2: " + repr(v2) + "   gamma2: " + repr(math.degrees(math.atan2(sgamma2, cgamma2))))

    def transfer(self):         # Add coordinates to transfer matrix
        self.__Transfer = np.vstack((self.__Transfer, self.plot_data()))

    def transfer_data(self):    # Get transfer data and reset matrix
        self.transfer()
        Temp = self.__Transfer
        self.__Transfer = np.empty(shape=(0,2))
        return Temp

