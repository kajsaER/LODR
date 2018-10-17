#!/usr/bin/python


from Subsystems import *
import math
import numpy as np
import matplotlib.pyplot as plt


orb = orbit()
orb.make(45e6, 0.9, math.radians(40))
deb1 = debris(0, 100, .1, 1, 0, orb, math.radians(60))

plt.figure()
deb1.plot('r')
plt.hold('on')
plt.plot(0, 0, '*')
deb1._orbit.Print()

for x in range(int(9e4)):
    deb1.step()
deb1.plot('g:')

laser = laser()
laser.switch(0)
antenna = antenna(12, 0.9)

atmosphere = atmosphere()

laser.fire(antenna, deb1, 10, atmosphere)
#deb1._orbit.plot_approx()
deb1.plot('b-.')
for x in range(1):
    deb1.step()
deb1._orbit.Print()

plt.show()
