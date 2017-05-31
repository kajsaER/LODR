#!/usr/bin/python

import math

a = 7000 #semi-major axis
b = 14000 #semi-minor axis
ep = float('nan') #eccentricity
f = float('nan') #focus
ra = float('nan') #apogee
rp = float('nan') #perigee
r = float('nan') #distance
nu = float('nan') #true anomaly
mu = 3.986e5 #gravity comstant of the Earth km^3/s^2]
T = 2*math.pi*math.sqrt(math.pow(a,3)/mu) #orbital period
Omega = float('nan') #right ascension
omega = float('nan') #argument of perigee
print T
