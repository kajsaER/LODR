#!/usr/bin/python

from __future__ import division
from Subsystems import *
import math
import numpy as np
import matplotlib.pyplot as plt



#r0 = 42164e3
#v0 = math.sqrt(consts.mu/r0)
#phi0 = math.radians(20)
#theta0 = math.pi - phi0

#nuw = math.radians(20)

orb = orbit()

#orb.find(r0, v0, theta0, nuw)
#orb.show()

orb.make(45e6, 0.8, math.radians(40))
deb1 = debris(0, 0, 1, 1, 0, orb, math.radians(60))
#orb.show2()
deb1.plot('b')

orb2 = orbit()
meas = deb1.measure()
orb2.find(meas['z'], meas['v'], meas['szeta'], meas['czeta'], meas['sgamma'], meas['cgamma'])

orb.Print()
orb2.Print()

orb2.plot_approx()
plt.hold('on')
deb1.plot('r:')
orb2.plot('g:')

plt.figure()
deb1.plot('r')
plt.hold('on')
orb2.plot('g:')
plt.show()
