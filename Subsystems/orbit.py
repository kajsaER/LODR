#!/usr/bin/python

from __future__ import division
import math
import constants as consts
import numpy as np

tol = 1e-4


class orbit:
    def __init__(self):
        self.a = float('nan') #semi-major axis
        #self.b = float('nan') #semi-minor axis
        self.ep = float('nan') #eccentricity
        #self.f = float('nan') #focus
        self.ra = float('nan') #apogee
        self.rp = float('nan') #perigee
        # debri self.r = float('nan') #distance
        # debris self.nu = float('nan') #true anomaly
        #constants self.mu = 3.986e5 #gravity comstant of the Earth km^3/s^2]
        #self.T = 2*math.pi*math.sqrt(math.pow(self.a,3)/consts.mu) #orbital period
        #self.Omega = float('nan') #right ascension
        #self.omega = float('nan') #argument of perigee
        

    def make(self, ra, rp):
        self.ra = ra #* 1.0
        self.rp = rp #* 1.0
        # Computations
        self.a = (self.ra + self.rp) / 2
        self.ep = (self.ra - self.rp) / (self.ra + self.rp)# * 1.0

    def find(self, v_r, v_t, r):
        self.a = 1 / (2/r - (math.pow(v_r, 2) + math.pow(v_t, 2))/consts.mu)
        eps = np.linspace(0, 1, 2000)
        found = False
        for ep in eps:
            if not found:
                q = self.a * (1 - math.pow(ep, 2))
                cosnu = 0
                if ep != 0:
                    cosnu = (q/r - 1) / ep
                if math.fabs(cosnu) < 1:
                    nu = math.acos(cosnu)
                    vt = math.sqrt(consts.mu/q) * (1 + ep * math.cos(nu))
                    vr = math.sqrt(consts.mu/q) * ep * math.sin(nu)
                    if math.fabs(vt - v_t) < tol:
                        if math.fabs(vr - v_r) < tol:
                            print "found orbit"
                            found = True
                            self.ep = ep
                            self.ra = self.a * (1 + self.ep)
                            self.rp = self.a * (1 - self.ep)
        

    def __del__(self):
        print "Orbit has been deleted"
        
