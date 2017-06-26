#!/usr/bin/python

from __future__ import division
from Subsystems import *
import math
import numpy as np
import matplotlib.pyplot as plt

#orb = orbit()
#print orb.T

#orb.make(40000, 13300)
#print orb.a
#print orb.ep

#v_r = 0.039694
#v_t = 0.151964
#r = 23362950

#orb.find(v_r, v_t, r)
#print "ep: " + repr(orb.ep)
#print "ra: " + repr(orb.ra)
#print "rp: " + repr(orb.rp)

r0 = 42164e3
v0 = math.sqrt(consts.mu/r0)
phi0 = math.radians(80)
theta0 = math.pi - phi0
dt = 5

E0 = 1/2 * math.pow(v0,2) - consts.mu/r0
L0 = r0*v0*math.sin(math.pi-phi0)

print "E0: " + repr(E0)
print "L0: " + repr(L0)

v = v0
r = r0
steps = int(1e5)
theta = theta0
phi = phi0
values = np.zeros((steps+1, 6))
values[0,:] = [v, v*math.cos(phi), v*math.sin(phi), r, phi, theta]
printed = np.zeros((steps+1))

for x in range(steps):
    
    v1 = v
    theta1 = theta
    r1 = r
    
    r2 = math.sqrt(math.pow(r1,2) + math.pow((v1*dt),2) - 2*r1*v1*dt*math.cos(theta1))
    v2 = math.sqrt(math.pow(v1,2) + 2*consts.mu*(1/r2 - 1/r1))
    sintheta = r1*v1/(r2*v2)*math.sin(theta1)

    if sintheta > 1 :
        #print x
        v2 = math.sqrt(math.pow(v1 - consts.mu/math.pow(r1,2)*math.cos(phi)*dt, 2) + math.pow(consts.mu/math.pow(r1,2)*math.sin(phi)*dt, 2))
        r2 = consts.mu / (1/2*(math.pow(v2,2) - math.pow(v1, 2)) + consts.mu/r1)
        sintheta = r1*v1/(r2*v2)*math.sin(theta1)
        if sintheta > 1 :
            print "Error, dt too big?"
            break

    theta2 = math.asin(sintheta)

    if math.fabs(math.pi/2 - theta2) < 0.002 and math.fabs(theta1-theta2) < 0.0001 :
        printed[x + 1] = True
        if printed[x] == False :
            print "D theta: " + repr(math.degrees(theta2-theta1)) + "   step: " + repr(x)
    
    if r2 > r1 and theta2 < math.pi/2 :
        theta2 = math.pi - theta2
    
    theta = theta2
    phi = math.pi - theta
    v = v2
    vr = v*math.cos(phi)
    vrn = v*math.sin(phi)
    r = r2
    
    row = np.array([v, vr, vrn, r, phi, math.degrees(theta)])
    values[x+1, :] = row


print "done"
x = range(steps+1)
Dtheta = math.fabs(90 - math.degrees(theta0))
V = values[: ,0]
VR = values[: ,1]
VRN = values[: ,2]
R = values[:, 3]
PHI = values[: , 4]
THETA = values[: , 5]

plt.figure(1)
plt.subplot(311)
plt.plot(x, R)
plt.title('Distance')
#plt.show()

#plt.figure(2)
plt.subplot(312)
plt.plot(x, THETA)
plt.title('Theta')
plt.axis([0, steps+1, 90-1.1*Dtheta, 90+1.1*Dtheta])

plt.subplot(313)
plt.plot(x, V)
plt.title('Velocity')
plt.show()


