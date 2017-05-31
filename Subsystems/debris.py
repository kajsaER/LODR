#!/usr/bin/python

class debris:
    def __init__(self, shape, material, size, mass, orientation):
        self.shape = shape
        self.material = material
        self.size = size
        self.mass = mass
        self.orientation = orientation

    def __del__(self):
        print "Debris deleted"
