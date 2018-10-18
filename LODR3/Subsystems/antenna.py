#!/usr/bin/python

class antenna:  # All the parameters which define the antenna

    def __init__(self, D, ratio):
        self.D = D              # Diameter
        self.ratio = ratio      # Ratio of usage
        self._Deff = D*ratio    # Effective diameter

    def Deff(self):         # Get effective diameter
        return self._Deff
        
    def set_D(self, value): # Set new diameter
        self.D = int(value)
        self._Deff = self.D*self.ratio

    def set_ratio(self, value): # Set new ratio
        self.ratio = value
        self._Deff = self.D*self.ratio
