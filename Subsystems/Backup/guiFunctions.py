#!/usr/bin/python

def changeLaser(self, i):
    self.LODR.laser.switch(i)

def radBtnState(self, b):

    if b.text() == "Frequency doubling":
        if b.ischecked() == True:
            self._laser.doubfreq()
        else:
            self._laser.normfreq()



