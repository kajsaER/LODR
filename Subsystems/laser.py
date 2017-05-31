#!/usr/bin/python

class laser:

    def __init__(self, power, wavelength):
        self.P = power #Power
        self.lambd = wavelength #Wavelength

        def __del__(self):
            print "Laser has been deleted"
