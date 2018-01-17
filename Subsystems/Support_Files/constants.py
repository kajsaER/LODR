#!/usr/bin/python

import math

h = 6.6261e-34 #Planck's constant [Js]
mu = 3.986e14 #gravity comstant of the Earth m^3/s^2]
Re = 6378e3 #Earth radius [m]


lat = -0.053683419 # GS latitude
slat = math.sin(lat)
clat = math.cos(lat)
# long = 0.651938653 # GS longitude
