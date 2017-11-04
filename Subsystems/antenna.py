#!/usr/bin/python

class antenna:
    'All the parameters which define the antenna'

    def __init__(self, D, ratio):
        self.D = D #
        self.ratio = ratio
        self._Deff = D*ratio

    def Deff(self):
        return self._Deff
        
    def __del__(self):
        print "Antenna deleted"
