from PyQt4 import QtCore, QtGui, uic
from ConfigParser import SafeConfigParser
import math, extmath, sys
import constants as consts
import numpy as np
from decimal import Decimal


qtCreatorLaser = "Subsystems/laser_widget.ui"
laser_widget, laserBaseClass = uic.loadUiType(qtCreatorLaser)
qtCreatorDefinedLaser = "Subsystems/definedLaser.ui"
DefinedLaserWidget, DefinedLaserBaseClass = uic.loadUiType(qtCreatorDefinedLaser)
qtCreatorUndefinedLaser = "Subsystems/undefinedLaser.ui"
UndefinedLaserWidget, UndefinedLaserBaseClass = uic.loadUiType(qtCreatorUndefinedLaser)

units = {'P':'W', 'W':'J','lambda':'m', 'frep':'Hz', 'tau':'s', 'T':'s'}



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
        
        self.slide_frep.actionTriggered.connect(lambda act: self.slide_trigged(act, 'frep'))
        self.slide_tau.actionTriggered.connect(lambda act: self.slide_trigged(act, 'tau'))
        self.slide_T.actionTriggered.connect(lambda act: self.slide_trigged(act, 'T'))
        self.slide_frep.sliderMoved.connect(lambda value: self.slide_moved(value, 'frep'))
        self.slide_tau.sliderMoved.connect(lambda value: self.slide_moved(value, 'tau'))
        self.slide_T.sliderMoved.connect(lambda value: self.slide_moved(value, 'T'))
        self.slide_frep.valueChanged.connect(lambda value: self.slide_changed(value, 'frep'))
        self.slide_tau.valueChanged.connect(lambda value: self.slide_changed(value, 'tau'))
        self.slide_T.valueChanged.connect(lambda value: self.slide_changed(value, 'T'))


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
        self.pot_frep = pow(10, temp[2])
        self.min_frep = extmath.myfloat(LaserType.get('repetition min'))
        self.scale_frep = extmath.myfloat(LaserType.get('repetition max'))-self.min_frep
        self.slide_frep.setValue((self.num_frep.value()*self.pot_frep-self.min_frep)*
                self.slide_frep.maximum()/self.scale_frep)

        temp = extmath.prefixedValue(LaserType.get('pulse duration'))
        self.num_tau.display(temp[1])
        self.unit_tau.setText(temp[0]+'s')
        self.pot_tau = pow(10, temp[2])
        self.min_tau = extmath.myfloat(LaserType.get('pulse min'))
        self.scale_tau = extmath.myfloat(LaserType.get('pulse max'))-self.min_tau
        self.slide_tau.setValue((self.num_tau.value()*self.pot_tau-self.min_tau)*
                self.slide_tau.maximum()/self.scale_tau)
        
        temp = extmath.prefixedValue(LaserType.get('fire duration'))
        self.num_T.display(temp[1])
        self.unit_T.setText(temp[0]+'s')
        self.pot_T = pow(10, temp[2])
        self.min_T = extmath.myfloat(LaserType.get('fire min'))
        self.scale_T = extmath.myfloat(LaserType.get('fire max'))-self.min_T
        self.slide_T.setValue((self.num_T.value()*self.pot_T-self.min_T)*
                self.slide_T.maximum()/self.scale_T)

    def double_freq(self):
        if self.freqDub.isChecked():
            self.main.lasersystem.doubfreq()
        else:
            self.main.lasersystem.normfreq()

    def slide_trigged(self, action, var):
        exec("%s" % 'val = self.slide_' + var + '.value()*self.scale_' +
                var + '/self.slide_' + var + '.maximum() + self.min_' + var)
        exec("%s" % 'pot = self.pot_' + var)
        exec("%s" % 'temp = extmath.prefixedValue(val)')
        exec("%s" % 'self.num_' + var + '.display(temp[1])')
        exec("%s" % 'self.unit_' + var + '.setText(temp[0] + units.get(var))')
        exec("%s" % 'self.pot_' + var + ' = pow(10, temp[2])')
        if var != 'T':
            exec("%s" % 'self.main.lasersystem._' + var + ' = val')

    def slide_moved(self, value, var):
        exec("%s" % 'val = value*self.scale_' + var + 
                '/self.slide_' + var + '.maximum() + self.min_' + var)
        exec("%s" % 'pot = self.pot_' + var)
        exec("%s" % 'temp = extmath.prefixedValue(val)')
        exec("%s" % 'self.num_' + var + '.display(temp[1])')
        exec("%s" % 'self.unit_' + var + '.setText(temp[0] + units.get(var))')
        exec("%s" % 'self.pot_' + var + ' = pow(10, temp[2])')

    def slide_changed(self, value, var):
        exec("%s" % 'val = value*self.scale_' + var + 
                '/self.slide_' + var + '.maximum() + self.min_' + var)
        exec("%s" % 'pot = self.pot_' + var)
        exec("%s" % 'temp = extmath.prefixedValue(val)')
        exec("%s" % 'self.num_' + var + '.display(temp[1])')
        exec("%s" % 'self.unit_' + var + '.setText(temp[0] + units.get(var))')
        exec("%s" % 'self.pot_' + var + ' = pow(10, temp[2])')
        if var != 'T':
            exec("%s" % 'self.main.lasersystem._' + var + ' = val')


class UndefinedLaser(UndefinedLaserBaseClass, UndefinedLaserWidget):
    def __init__(self, main, parent=None):
        super(UndefinedLaser, self).__init__(parent)
        self.setupUi(self)
        self.main = main
        self.main.laserConf.add_section('Custom')
        if 'Custom' not in self.main.laser_type_list:
            self.main.laserType.addItem('Custom')
            self.main.laser_type_list.append('Custom')
        LT = {'Power':'1000', 'Power min':'0', 'Power max':'1e6',
              'Energy':'0', 'Energy min':'0', 'Energy max':'1',
              'Lambda':'0', 'Lambda min':'0', 'Lambda max':'1', 
              'M2':'1', 'M2 min':'1', 'M2 max':'1e2',
              'Cb':'1', 'Cb min':'1', 'Cb max':'1e1',
              'Repetition rate':'0', 'Pulse duration':'0'}
        for name in LT.keys():
            self.main.laserConf.set('Custom', name, LT[name])


        self.freqDub.toggled.connect(self.double_freq)
        
        self.slide_P.actionTriggered.connect(lambda act: self.slide_trigged(act, 'P'))
        self.slide_W.actionTriggered.connect(lambda act: self.slide_trigged(act, 'W'))
        self.slide_lambda.actionTriggered.connect(lambda act: self.slide_trigged(act, 'lambda'))
        self.slide_M2.actionTriggered.connect(lambda act: self.slide_trigged(act, 'M2'))
        self.slide_Cb.actionTriggered.connect(lambda act: self.slide_trigged(act, 'Cb'))
        self.slide_frep.actionTriggered.connect(lambda act: self.slide_trigged(act, 'frep'))
        self.slide_tau.actionTriggered.connect(lambda act: self.slide_trigged(act, 'tau'))
        self.slide_T.actionTriggered.connect(lambda act: self.slide_trigged(act, 'T'))
        self.slide_frep.sliderMoved.connect(lambda value: self.slide_moved(value, 'frep'))
        self.slide_tau.sliderMoved.connect(lambda value: self.slide_moved(value, 'tau'))
        self.slide_T.sliderMoved.connect(lambda value: self.slide_moved(value, 'T'))
        self.slide_frep.valueChanged.connect(lambda value: self.slide_changed(value, 'frep'))
        self.slide_tau.valueChanged.connect(lambda value: self.slide_changed(value, 'tau'))
        self.slide_T.valueChanged.connect(lambda value: self.slide_changed(value, 'T'))

    def build_unit_box(self, measure):
        listed = []
        if measure in {'P', 'frep'}:
            for pref in ['', 'k', 'M', 'G']:
                listed.append(unicode(pref + units.get(measure)))
            exec("%s" % 'self.unit_' + measure + '.addItems(listed)')
        elif measure in {'W', 'lambda', 'tau'}:
            for pref in ['', 'm', u'\u03bc', 'n']:
                listed.append(unicode(pref + units.get(measure)))
            exec("%s" % 'self.unit_' + measure + '.addItems(listed)')
        elif measure in {'T'}:
            for pref in ['', 'm', u'\u03bc']:
                listed.append(unicode(pref + units.get(measure)))
            exec('self.unit_' + measure + '.addItems(listed)')


    def setDefaultLaserParam(self, LaserType):
        self.freqDub.setChecked(False)
        self.LaserType = LaserType

        self.set_default_value('power', 'P')
        self.set_default_value('energy', 'W')
        self.set_default_value('lambda', 'lambda')

        self.num_M2.display(float(LaserType.get('m2')))
        self.num_Cb.display(float(LaserType.get('cb')))
        
        self.set_default_value('repetition rate', 'frep')
        self.set_default_value('pulse duration', 'tau')
        self.set_default_value('fire duration', 'T')

    def set_default_value(self, LONG, SHORT):
        temp = extmath.prefixedValue(self.LaserType.get(LONG))
        exec('self.num_' + SHORT + '.display(temp[1])')
        self.build_unit_box(SHORT)
        pot = pow(10, temp[2])
        exec('self.pot_' + SHORT + ' = pot')
        if pot != 1:
            self.set_unit(SHORT)
        exec('self.min_'+SHORT+' = extmath.myfloat(self.LaserType.get(str(LONG + \' min\')))')
        exec('self.scale_'+SHORT+' = extmath.myfloat(self.LaserType.get(str(LONG + \' max\')))-self.min_' + SHORT)
        exec('self.slide_'+SHORT+'.setValue((self.num_'+SHORT+'.value()*pot-self.min_'+SHORT+')*self.slide_'+SHORT+'.maximum()/self.scale_'+SHORT+')')

    def set_unit(self, var):
        exec('p = self.pot_' + var)
        power = '%.0E' % Decimal(p)
        prefixedunit = extmath.allPot.get(power) + units.get(var)
#        print prefixedunit
        exec('unit = self.unit_' + var)
        for ind in range(0, unit.count()-1):
            if unit.itemText(ind) == prefixedunit:
                unit.setCurrentIndex(ind)
                break

    def double_freq(self):
        if self.freqDub.isChecked():
            self.main.lasersystem.doubfreq()
        else:
            self.main.lasersystem.normfreq()

    def slide_trigged(self, action, var):
        exec("%s" % 'val = self.slide_' + var + '.value()*self.scale_' +
                var + '/self.slide_' + var + '.maximum() + self.min_' + var)
        if var not in {'M2', 'Cb'}:
            exec("%s" % 'pot = self.pot_' + var)
            exec("%s" % 'temp = extmath.prefixedValue(val)')
            exec("%s" % 'self.num_' + var + '.display(temp[1])')
            exec("%s" % 'self.unit_' + var + '.setText(temp[0] + units.get(var))')
            exec("%s" % 'self.pot_' + var + ' = pow(10, temp[2])')
        else:
            exec("%s" % 'self.num_' + var + '.display(val)')
        if var != 'T':
            exec("%s" % 'self.main.lasersystem._' + var + ' = val')

    def slide_moved(self, value, var):
        exec("%s" % 'val = value*self.scale_' + var + 
                '/self.slide_' + var + '.maximum() + self.min_' + var)
        exec("%s" % 'pot = self.pot_' + var)
        exec("%s" % 'temp = extmath.prefixedValue(val)')
        exec("%s" % 'self.num_' + var + '.display(temp[1])')
        exec("%s" % 'self.unit_' + var + '.setText(temp[0] + units.get(var))')
        exec("%s" % 'self.pot_' + var + ' = pow(10, temp[2])')

    def slide_changed(self, value, var):
        exec("%s" % 'val = value*self.scale_' + var + 
                '/self.slide_' + var + '.maximum() + self.min_' + var)
        exec("%s" % 'pot = self.pot_' + var)
        exec("%s" % 'temp = extmath.prefixedValue(val)')
        exec("%s" % 'self.num_' + var + '.display(temp[1])')
        exec("%s" % 'self.unit_' + var + '.setText(temp[0] + units.get(var))')
        exec("%s" % 'self.pot_' + var + ' = pow(10, temp[2])')
        if var != 'T':
            exec("%s" % 'self.main.lasersystem._' + var + ' = val')
