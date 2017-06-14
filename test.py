#!/usr/bin/python

from Subsystems import *



orb = orbit()
#print orb.T

#orb.make(40000, 13300)
#print orb.a
#print orb.ep

v_r = 0.039694
v_t = 0.151964
r = 23362950

orb.find(v_r, v_t, r)
print "ep: " + repr(orb.ep)
print "ra: " + repr(orb.ra)
print "rp: " + repr(orb.rp)
