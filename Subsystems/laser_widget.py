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
        temp = extmath.prefixedValue(LaserType.get('power'))
        self.num_P.display(temp[1])
        self.unit_P.setText(temp[0]+'W')

        temp = extmath.prefixedValue(LaserType.get('energy'))
        self.num_W.display(temp[1])
        self.unit_W.setText(temp[0]+'J')

        temp = extmath.prefixedValue(LaserType.get('lambda'))
        self.num_lambda.display(temp[1])
        self.unit_lambda.setText(temp[0]+'m')

        self.num_M2.display(float(LaserType.get('m2')))
        self.num_Cb.display(float(LaserType.get('cb')))
        
        temp = extmath.prefixedValue(LaserType.get('repetition rate'))
        self.num_frep.display(temp[1])
        self.unit_frep.setText(temp[0]+'Hz')
        self.frep_min = extmath.myfloat(LaserType.get('repetition min'))
        self.slide_frep.setMinimum()
        self.slide_frep.setMaximum()
        self.slide_frep.setValue(self.num_frep.value())

        temp = extmath.prefixedValue(LaserType.get('pulse duration'))
        self.num_tau.display(temp[1])
        self.unit_tau.setText(temp[0]+'s')
        self.tau_min = extmath.prefixedValue(LaserType.get('pulse min'))[1]
        self.tau_scale = extmath.prefixedValue(LaserType.get('pulse max'))[1]-self.tau_min
        self.slide_tau.setValue((self.num_tau.value()-self.tau_min)*self.slide_tau.maximum()/
                self.tau_scale)
        # self.num_T.display(LaserType.get(''))
        # self.slide_T

    def double_freq(self):
        if self.freqDub.isChecked():
            main.lasersystem.doubfreq()
        else:
            main.lasersystem.normfreq()

class UndefinedLaser(UndefinedLaserBaseClass, UndefinedLaserWidget):
    def __init__(self, main, parent=None):
        super(UndefinedLaser, self).__init__(parent)
        self.setupUi(self)
        self.main = main
        self.main.laserConf.add_section('Custom')
        if 'Custom' not in self.main.laser_type_list:
            self.main.laserType.addItem('Custom')
            self.main.laser_type_list.append('Custom')
        LT = {'Power':'0', 'Power min':'0', 'Power max':'1e6', 'Energy':'0', 'Lambda':'0', 'M2': '0', 'Cb':'0',
                'Repetition rate':'0', 'Pulse duration':'0'}
        for name in LT.keys():
            self.main.laserConf.set('Custom', name, LT[name])

    def setDefaultLaserParam(self, LaserType):
        self.freqDub.setChecked(False)
        self.num_P.display(float(LaserType.get('power')))
        self.num_W.display(float(LaserType.get('energy')))
        self.num_lambda.display(float(LaserType.get('lambda')))
        self.num_M2.display(float(LaserType.get('m2')))
        self.num_Cb.display(float(LaserType.get('cb')))
        self.num_frep.display(float(LaserType.get('repetition rate')))
        # self.slide_frep
        self.num_tau.display(float(LaserType.get('pulse duration')))
        # self.slide_tau
        # self.num_T.display(LaserType.get(''))
        # self.slide_T

