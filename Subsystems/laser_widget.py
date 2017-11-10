from PyQt4 import QtCore, QtGui, uic
from ConfigParser import SafeConfigParser
import math, extmath
import constants as consts
import numpy as np

qtCreatorLaser = "Subsystems/laser_widget.ui"
laser_widget, laserBaseClass = uic.loadUiType(qtCreatorLaser)
qtCreatorDefinedLaser = "Subsystems/definedLaser.ui"
DefinedLaserWidget, DefinedLaserBaseClass = uic.loadUiType(qtCreatorDefinedLaser)
qtCreatorUndefinedLaser = "Subsystems/undefinedLaser.ui"
UndefinedLaserWidget, UndefinedLaserBaseClass = uic.loadUiType(qtCreatorUndefinedLaser)

class Laser_Widget(laserBaseClass, laser_widget):
    def __init__(self, main, parent=None):
        super(Laser_Widget, self).__init__(parent)
        self.setupUi(self)
        self.main = main


class DefinedLaser(DefinedLaserBaseClass, DefinedLaserWidget):
    def __init__(self, main, parent=None):
        super(DefinedLaser, self).__init__(parent)
        self.setupUi(self)
        self.main = main

        self.freqDub.toggled.connect(self.double_freq)

    def setDefaultLaserParam(self, LaserType):
        self.freqDub.setChecked(False)
        self.num_P.display(LaserType.get('power'))
        self.num_W.display(LaserType.get('energy'))
        self.num_lambda.display(float(LaserType.get('lambda')))
        self.num_M2.display(LaserType.get('m2'))
        self.num_Cb.display(LaserType.get('cb'))
        self.num_frep.display(LaserType.get('repetition rate'))
        # self.slide_frep
        self.num_tau.display(LaserType.get('pulse duration'))
        # self.slide_tau
        # self.num_T.display(LaserType.get(''))
        # self.slide_T

    def double_freq(self):
        if self.freqDub.isChecked():
            print 'Yes'
        else:
            print 'No'

class UndefinedLaser(UndefinedLaserBaseClass, UndefinedLaserWidget):
    def __init__(self, main, parent=None):
        super(UndefinedLaser, self).__init__(parent)
        self.setupUi(self)
        self.main = main

