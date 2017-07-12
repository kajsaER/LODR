#!/usr/bin/python

from __future__ import division
import math
import constants as consts
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
        self.vals = 0 #np.zeros((int(1e6+1), 7))
        #debris self.nu = float('nan') #true anomaly
        #self.T = 2*math.pi*math.sqrt(math.pow(self.a,3)/consts.mu) #orbital period
        #self.Omega = float('nan') #right ascension
        self.omega = float('nan') #argument of perigee
        

    def make(self, a, ep, omega):
        self.a = a
        self.ep = ep
        self.omega = omega
        # Computations
        self.ra = self.a*(1 + self.ep)
        self.rp = self.a*(1 - self.ep)
        self.b = self.a*math.sqrt(1 - math.pow(ep,2))

    def find(self, r, v, theta, nuw) :
        st = math.sin(theta)
        ct = math.cos(theta)
        snuw = math.sin(nuw)
        cnuw = math.cos(nuw)
        dt = 1
        
        steps = int(1e6)
        self.vals = np.zeros((steps+1, 7))
        self.vals[0, :] = [v, -v*ct, v*st, r, math.degrees(math.acos(ct)), r*cnuw, r*snuw]
        
        for x in range(steps) :
            v1 = v
            r1 = r
            st1 = st
            ct1 = ct
            
            v2 = math.sqrt(math.pow(v1 + consts.mu/math.pow(r1,2)*ct1*dt, 2) + 
                           math.pow(consts.mu/math.pow(r1,2)*st1*dt, 2))
            r2 = consts.mu / (1/2*(math.pow(v2, 2) - math.pow(v1, 2)) + consts.mu / r1)
            st2 = r1*v1/(r2*v2)*st1
           
            if math.fabs(st2) >= 1 :
                r2 = math.sqrt(math.pow(r1, 2) + math.pow(v1*dt, 2) - 2*r1*v1*dt*ct1)
                v2 = math.sqrt(math.pow(v1, 2) + 2*consts.mu*(1/r2 - 1/r1))
                st2 = r1*v1/(r2*v2)*st1
           
            if math.fabs(st2) >=1 :
                print "Error, dt too big?"
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
            
            row = np.array([v, vr, vrn, r, math.degrees(math.acos(ct)), r*cnuw, r*snuw])
            self.vals[x+1, :] = row
            
    def show_approx(self):
        self.plot_approx()
        plt.show()

    def plot_approx(self):
        steps = self.vals.shape[0]
        x = range(steps)
        V = self.vals[:, 0]
        VR = self.vals[:, 1]
        VRN = self.vals[:, 2]
        R = self.vals[:, 3]
        THETA = self.vals[:, 4]
        X = self.vals[:, 5]
        Y = self.vals[:, 6]
        Dtheta = np.fmax(math.fabs(90 - np.amin(THETA)), math.fabs(np.amax(THETA) - 90))

        plt.figure()
        plt.subplot(311)
        plt.plot(x, R)
        plt.title('Distance')
        
        plt.subplot(312)
        plt.plot(x, THETA)
        plt.title('Theta')
        plt.axis([0, steps, 90-1.1*Dtheta, 90+1.1*Dtheta])

        plt.subplot(313)
        plt.plot(x, V)
        plt.title('Velocity')

        plt.figure()
        plt.plot(X, Y)
        plt.axis('equal')

    def plot(self, line):
        X = np.zeros((360, 1))
        Y = np.zeros((360, 1))
        for l in range(0, 360):
            phi = l*math.pi/180
            ang = self.omega + phi
            r = self.a * (1 - math.pow(self.ep, 2)) / (1 + self.ep*math.cos(phi))
            X[l] = r*math.cos(ang)
            Y[l] = r*math.sin(ang)
        
#       plt.figure()
        plt.plot(X,Y, line)
        plt.axis('equal')
    
    def __del__(self):
        print "Orbit has been deleted"
