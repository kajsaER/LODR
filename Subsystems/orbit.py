#!/usr/bin/python

import math

class orbit:
    def __init__(self):
        self.a = 7000 #semi-major axis
        self.b = 14000 #semi-minor axis
        self.ep = float('nan') #eccentricity
        self.f = float('nan') #focus
        self.ra = float('nan') #apogee
        self.rp = float('nan') #perigee
        self.r = float('nan') #distance
        self.nu = float('nan') #true anomaly
        self.mu = 3.986e5 #gravity comstant of the Earth km^3/s^2]
        self.T = 2*math.pi*math.sqrt(math.pow(self.a,3)/self.mu) #orbital period
        self.Omega = float('nan') #right ascension
        self.omega = float('nan') #argument of perigee


        def __del__(self):
            print "Orbit has been deleted"
