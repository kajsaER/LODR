#!/usr/bin/python

from __future__ import division
from Subsystems import *
import math
import numpy as np
import matplotlib.pyplot as plt



r0 = 42164e3
v0 = math.sqrt(consts.mu/r0)
phi0 = math.radians(70)
theta0 = math.pi - phi0

nuw = math.radians(20)

orb = orbit()

orb.find(r0, v0, theta0, nuw)
orb.show()
