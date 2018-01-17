#!/usr/bin/python

from __future__ import division
import math
import Support_Files.extmath as extmath
import Support_Files.constants as consts
import numpy as np
import matplotlib.pyplot as plt

tol = 1e-4


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
#        self.a = a
        self.rp = rp
        self.ep = ep
        self.omega = omega
        # Computations
        self.a = self.rp/(1 - self.ep)
        self.ra = self.a*(1 + self.ep)
#        self.rp = self.a*(1 - self.ep)
        self.b = self.a*math.sqrt(1 - math.pow(ep,2))
        self.v0 = math.sqrt(consts.mu*(2/self.rp - 1/self.a))
        self.cw = math.cos(self.omega)
        self.sw = math.sin(self.omega)
        self.T = 2*math.pi*math.sqrt(math.pow(self.a,3)/consts.mu) #orbital period
        self.n = 2*math.pi/self.T
 
    def find(self, z, v, szeta, czeta, sbeta, cbeta):
        salpha = extmath.sinplus(sbeta, cbeta, 1, 0)
        calpha = extmath.cosplus(sbeta, cbeta, 1, 0)
        r = math.sqrt(math.pow(consts.Re, 2) + math.pow(z, 2) - 2*consts.Re*z*calpha)
        cphi = (math.pow(consts.Re, 2) + math.pow(r, 2) - math.pow(z, 2)) / (2*consts.Re*r)
        sphi = z/r*salpha
        cdelta = (math.pow(z, 2) + math.pow(r, 2) - math.pow(consts.Re, 2)) / (2*r*z)
        sdelta = consts.Re/r*salpha

        st = extmath.sinplus(sdelta, cdelta, szeta, czeta)
        ct = extmath.cosplus(sdelta, cdelta, szeta, czeta)
        snuw = extmath.sinminus(consts.slat, consts.clat, sphi, cphi)
        cnuw = extmath.cosminus(consts.slat, consts.clat, sphi, cphi)

        dt1 = 1
        t = 0
        
        steps = int(8e5)
        self.__vals = np.zeros((steps+1, 9))
        self.__vals[0, :] = ([v, -v*ct, v*st, r, math.degrees(math.acos(ct)),
                              r*cnuw, r*snuw, dt1, t])
        
        nuw = math.atan2(snuw, cnuw)
        x = 1
        passes = 0
#        for x in range(steps):
        while passes < 5:
            v1 = v
            r1 = r
            st1 = st
            ct1 = ct
            dt = dt1

            dvn = consts.mu/math.pow(r1, 2)*st1*dt
            dvt = consts.mu/math.pow(r1, 2)*ct1*dt

            while math.fabs(dvt) <= 1e-4 and dt <= 30:
                dt = dt + .1
                dvn = consts.mu/math.pow(r1, 2)*st1*dt
                dvt = consts.mu/math.pow(r1, 2)*ct1*dt
            
            if math.fabs(dvt) <= 1e-4:
                dt = dt1
                dvn = consts.mu/math.pow(r1, 2)*st1*dt
                dvt = consts.mu/math.pow(r1, 2)*ct1*dt
 
            v2 = math.sqrt(math.pow(v1 + dvt, 2) + math.pow(dvn, 2))
            r2 = consts.mu / (1/2*(math.pow(v2, 2) - math.pow(v1, 2)) + consts.mu / r1)
            st2 = r1*v1/(r2*v2)*st1
           
            if math.fabs(st2) > 1 :
                st2a = st2
                r2 = math.sqrt(math.pow(r1, 2) + math.pow(v1*dt, 2) - 2*r1*v1*dt*ct1)
                v2 = math.sqrt(math.pow(v1, 2) + 2*consts.mu*(1/r2 - 1/r1))
                st2 = r1*v1/(r2*v2)*st1
            else :
                st2a = -st2
            
            if st2 == st2a:
                st2 = 1
                v2 = v1
                r2 = r1

            if math.fabs(st2) > 1: 
                print "st2= " + repr(st2) + ",  dt= " + repr(dt) + " too big?" 
                break
            
            ct2 = math.sqrt(1-math.pow(st2, 2))
            
            if (r2 >= r1 and ct2 > 0) or (r2 <= r1 and ct2 < 0) :
                ct2 = -ct2
            
            sa = st1/r1*v1*dt
            if sa >= 1:
                print 'sa: ' + repr(sa) +  ',  x: ' + repr(x)
                break
            ca = math.sqrt(1-math.pow(sa, 2))
            cnuw2 = cnuw*ca-snuw*sa
            snuw2 = snuw*ca+cnuw*sa
            
            ct = ct2
            st = st2
            v = v2
            vr = -v*ct
            vrn = v*st
            r = r2
            snuw = snuw2
            cnuw = cnuw2
            
            nuw_old = nuw
            nuw = math.atan2(snuw, cnuw)
            t = t+dt
            
            if (nuw*nuw_old) < 0:
                passes += 1

            row = np.array([v, vr, vrn, r, math.degrees(math.acos(ct)), r*cnuw, r*snuw, dt, t])
            self.__vals[x, :] = row
            x += 1
        self.__vals = self.__vals[0:x-1, :]
        R = self.__vals[:, 3]
        VR = self.__vals[:, 1]
        zer = np.zeros(1)
        temp = np.concatenate((zer, VR), axis=0)*np.concatenate((VR, zer), axis=0)
        turns = np.where(temp<0)[0]
        self.rp = np.amin(R)
        self.ra = np.amax(R)
        self.a = (self.ra + self.rp)/2
        self.ep = (self.ra-self.rp)/(self.ra+self.rp)
        self.b = self.a*math.sqrt(1 - math.pow(self.ep, 2))
        self.v0 = math.sqrt(consts.mu*(2/self.rp - 1/self.a))
        if turns.shape[0] > 1 :
            mini = turns[0]
            if R[turns[1]] < R[mini]:
                mini = turns[1]
            self.cw = self.__vals[mini-1, 5]/self.rp
            self.sw = math.sqrt(1 - math.pow(self.cw, 2))
            self.omega = math.atan2(self.sw, self.cw)
        else :
            self.cw = 1
            self.sw = 0
            self.omega = 0.0
        self.T = 2*math.pi*math.sqrt(math.pow(self.a,3)/consts.mu) #orbital period
        self.n = 2*math.pi/self.T
 
            
#    def show_approx(self):
#        self.plot_approx()
#        plt.show()

    def plot_approx_data(self):
#        steps = self.__vals.shape[0]
#        x = range(steps)
        V = self.__vals[:, 0]
        VR = self.__vals[:, 1]
        VRN = self.__vals[:, 2]
        R = self.__vals[:, 3]
        GAMMA = self.__vals[:, 4]
        X = self.__vals[:, 5]
        Y = self.__vals[:, 6]
        DT = self.__vals[:, 7]
        T = self.__vals[:, 8]
        Dgamma = np.fmax(math.fabs(90 - np.amin(GAMMA)), math.fabs(np.amax(GAMMA) - 90))

#        plt.plot(X, Y)
#        plt.axis('equal')
        return [X, Y]

#    def plot(self, line):
#        X = np.zeros((360, 1))
#        Y = np.zeros((360, 1))
#        for l in range(0, 360):
#            phi = l*math.pi/180
#            ang = self.omega + phi
#            r = self.a * (1 - math.pow(self.ep, 2)) / (1 + self.ep*math.cos(phi))
#            X[l] = r*math.cos(ang)
#            Y[l] = r*math.sin(ang)
#        
#        plt.plot(X,Y, line)
#        plt.axis('equal')

    def plot_data(self):
        X = np.zeros((360, 1))
        Y = np.zeros((360, 1))
        for l in range(0, 360):
            phi = l*math.pi/180
            ang = self.omega + phi
            r = self.a * (1 - math.pow(self.ep, 2)) / (1 + self.ep*math.cos(phi))
            X[l] = r*math.cos(ang)
            Y[l] = r*math.sin(ang)
        return [X, Y]        

    def Print(self):
        print "Semi-major axis, a: " + repr(self.a)
        print "Semi-minor axis, b: " + repr(self.b)
        print "Eccentricity, ep: " + repr(self.ep)
        print "Appogee, ra: " + repr(self.ra)
        print "Perigee, rp: " + repr(self.rp)
        print "Argument of perigee, w: " + repr(self.omega)
        print "T: " + repr(self.T)
    
#    def __del__(self):
#        print "Orbit has been deleted"
