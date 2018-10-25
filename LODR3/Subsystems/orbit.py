#!/usr/bin/python


import math
from .Support_Files import constants as consts
from .Support_Files import extmath
import numpy as np
import matplotlib.pyplot as plt

tol = 1e-4      # Tolerance for 0


class orbit:
    def __init__(self):
        self.a = float('nan') #semi-major axis
        self.b = float('nan') #semi-minor axis
        self.ep = float('nan') #eccentricity
        self.ra = float('nan') #apogee
        self.rp = float('nan') #perigee
        self.__vals = 0 #np.zeros((int(1e6+1), 7))
        self.omega = float('nan') #argument of perigee

    def make(self, rp, ep, omega):
        self.rp = rp
        self.ep = ep
        self.omega = omega
        # Computations
        self.a = self.rp/(1 - self.ep)
        self.ra = self.a*(1 + self.ep)
        self.b = self.a*math.sqrt(1 - math.pow(ep,2))
        self.vp = math.sqrt(consts.mu*(2/self.rp - 1/self.a))   # Vis-viva
        self.cw = math.cos(self.omega)
        self.sw = math.sin(self.omega)
        self.n = math.sqrt(consts.mu/math.pow(self.a, 3))   # Mean angular velocity  2*math.pi/self.T
 
    def find(self, z, v, szeta, czeta, sbeta, cbeta):       # Find an orbit that fits the measurements
        sxi = extmath.sinplus(sbeta, cbeta, 1, 0)
        cxi = extmath.cosplus(sbeta, cbeta, 1, 0)
        r = math.sqrt(math.pow(consts.Re, 2) + math.pow(z, 2) - 2*consts.Re*z*cxi) # Law of Cosines
        cphi = (math.pow(consts.Re, 2) + math.pow(r, 2) - math.pow(z, 2)) / (2*consts.Re*r)
        sphi = z/r*(-sxi)                                # Law of Sines
        cdelta = (math.pow(z, 2) + math.pow(r, 2) - math.pow(consts.Re, 2)) / (2*r*z)
        sdelta = consts.Re/r*sxi

        sgamma = extmath.sinplus(sdelta, cdelta, szeta, czeta)
        cgamma = extmath.cosplus(sdelta, cdelta, szeta, czeta)
        snuw = extmath.sinplus(consts.slat, consts.clat, sphi, cphi)
        cnuw = extmath.cosplus(consts.slat, consts.clat, sphi, cphi)
        
        dt1 = 1
        t = 0
        
        steps = int(8e5)
        self.__vals = np.zeros((steps+1, 9))            # Make a matrix to store values in
        self.__vals[0, :] = ([v, -v*cgamma, v*sgamma, r, math.degrees(math.atan2(sgamma, cgamma)),
                              r*cnuw, r*snuw, dt1, t])  # Store starting values
        
        nuw = math.atan2(snuw, cnuw)
        x = 1
        passes = 0
        
        while passes < 3:       # Run for at least one whole orbit
            v1 = v
            r1 = r
            sgamma1 = sgamma
            cgamma1 = cgamma
            dt = dt1

            dvn = consts.mu/math.pow(r1, 2)*sgamma1*dt      # Effect of Earth gravity on the velocity of the debris
            dvt = consts.mu/math.pow(r1, 2)*cgamma1*dt

            while math.fabs(dvt) <= tol and dt <= 30:       # If the change is almost 0 increas the time step until
                dt = dt + .1                                # either the change is big enough or the time step is
                dvn = consts.mu/math.pow(r1, 2)*sgamma1*dt  # too big.
                dvt = consts.mu/math.pow(r1, 2)*cgamma1*dt
            
            if math.fabs(dvt) <= tol:                       # If the increas didn't help, use original time step
                dt = dt1
                dvn = consts.mu/math.pow(r1, 2)*sgamma1*dt
                dvt = consts.mu/math.pow(r1, 2)*cgamma1*dt
 
            v2 = math.sqrt(math.pow(v1 + dvt, 2) + math.pow(dvn, 2))
            r2 = consts.mu / (1/2*(math.pow(v2, 2) - math.pow(v1, 2)) + consts.mu / r1) # Constant Energy
            sgamma2 = r1*v1/(r2*v2)*sgamma1                 # Law of Sines
           
            if math.fabs(sgamma2) > 1 :                     # If gamma is impossible
                sgamma2a = sgamma2
                r2 = math.sqrt(math.pow(r1, 2) + math.pow(v1*dt, 2) - 2*r1*v1*dt*cgamma1)   # Law of Cosines
                v2 = math.sqrt(math.pow(v1, 2) + 2*consts.mu*(1/r2 - 1/r1))                 # Constant Energy
                sgamma2 = r1*v1/(r2*v2)*sgamma1                                             # Law of Sines
            else :
                sgamma2a = -sgamma2                         # Else store -gamma
            
            if sgamma2 == sgamma2a:                         # If they are the same value assume it's a circular orbit
                sgamma2 = 1
                v2 = v1
                r2 = r1

            if math.fabs(sgamma2) > 1:                      # If it's still impossible, generate error message.
                raise Exception("sgamma2= " + repr(sgamma2) + ",  dt= " + repr(dt) + " too big?") 
                break
            
            cgamma2 = math.sqrt(1-math.pow(sgamma2, 2))     # Pythagorean trigonometric identity
            
            if (r2 >= r1 and cgamma2 > 0) or (r2 <= r1 and cgamma2 < 0) :   # Check if gamma is >90 or <90
                cgamma2 = -cgamma2                                          # and adjust if needed
            
            sdnu = sgamma1/r2*v1*dt                         # Law of Sines
            if sdnu >= 1:                                   # If impossible value, rais error message
                raise Exception('sin(dnu): ' + repr(sdnu) +  ',  x: ' + repr(x))
                break

            cdnu = math.sqrt(1-math.pow(sdnu, 2))           # cos(dnu) should always be positive because dnu is small
            cnuw2 = extmath.cosplus(snuw, cnuw, sdnu, cdnu) # new nu + omega = old nu + omega + dnu
            snuw2 = extmath.sinplus(snuw, cnuw, sdnu, cdnu)
            
            cgamma = cgamma2                                # Store values for next iteration
            sgamma = sgamma2
            v = v2
            vr = -v*cgamma
            vrn = v*sgamma
            r = r2
            snuw = snuw2
            cnuw = cnuw2
            
            nuw_old = nuw
            nuw = math.atan2(snuw, cnuw)
            t = t+dt
            
            if (nuw*nuw_old) < 0:           # Check if the equator has been crossed
                passes += 1

            row = np.array([v, vr, vrn, r, math.degrees(math.atan2(sgamma, cgamma)), r*cnuw, r*snuw, dt, t])
            self.__vals[x, :] = row         # Store iteration values in matrix for later use
            x += 1

        self.__vals = self.__vals[0:x-1, :] # Use only relevant rows
        R = self.__vals[:, 3]               # Vector of radius values
        VR = self.__vals[:, 1]              # Vector of radial velocity values
        zer = np.zeros(1)                   # [0 Vr]*[Vr 0] to find where the orbit has its turning points
        temp = np.concatenate((zer, VR), axis=0)*np.concatenate((VR, zer), axis=0)
        turns = np.where(temp<0)[0]
        self.rp = np.amin(R)
        self.ra = np.amax(R)
        self.a = (self.ra + self.rp)/2
        self.ep = (self.ra-self.rp)/(self.ra+self.rp)
        self.b = self.a*math.sqrt(1 - math.pow(self.ep, 2))
        self.vp = math.sqrt(consts.mu*(2/self.rp - 1/self.a))   # Vis-viva
        if turns.shape[0] > 1 :             # If there are turning points check if apogee or perigee
            mini = turns[0]                 # comes first
            if R[turns[1]] < R[mini]:
                mini = turns[1]
            self.cw = self.__vals[mini-1, 5]/self.rp    # Get argument of perigee
            self.sw = self.__vals[mini-1, 6]/self.rp
            self.omega = math.atan2(self.sw, self.cw)
        else :                              # If there are no turning points
            self.cw = 1                     # circular orbit with 0 degree argument of perigee
            self.sw = 0
            self.omega = 0.0
        
        self.n = math.sqrt(consts.mu/math.pow(self.a, 3))   # Mean angular velocity
    
            
    def plot_approx_data(self):     # Get data points for plotting the approximation process
        X = self.__vals[:, 5]
        Y = self.__vals[:, 6]
        return [X, Y]


    def plot_data(self):            # Get plot data point for defined orbit
        X = np.zeros((360, 1))
        Y = np.zeros((360, 1))
        for l in range(0, 360):
            nu  = l*math.pi/180
            ang = self.omega + nu
            r = self.a * (1 - math.pow(self.ep, 2)) / (1 + self.ep*math.cos(nu))
            X[l] = r*math.cos(ang)
            Y[l] = r*math.sin(ang)
        return [X, Y]        

    def get_data(self):             # Get variable values
        string = ("Semi-major axis, a: " + repr(self.a) + "\n" +
                  "Semi-minor axis, b: " + repr(self.b) + "\n" +
                  "Eccentricity, ep: " + repr(self.ep) + "\n" +
                  "Appogee, ra: " + repr(self.ra) + "\n" +
                  "Perigee, rp: " + repr(self.rp) + "\n" +
                  "Argument of perigee, w: " + repr(self.omega) + "\n")
        return string
