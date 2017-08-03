#!/usr/bin/ython

from __future__ import division
from Subsystems import *
import math
import numpy as np
import matplotlib.pyplot as plt


orb = orbit()
orb.make(45e6, 0.8, math.radians(40))
deb1 = debris(0, 100, .1, 1, 0, orb, math.radians(60))

plt.figure()
deb1.plot('r')
plt.hold('on')
plt.plot(0, 0, '*')

for x in range(int(9e4)):
    deb1.step()
deb1.plot('g:')

laser = laser()
laser.switch(0)

bm = beam(laser, 1.7, 10, 5e-7, 10e7)
bm.fire(deb1, 1.0)

for x in range(1):
    deb1.step()

deb1.plot('b-.')

plt.show()
