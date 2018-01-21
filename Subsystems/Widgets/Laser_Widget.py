from PyQt4 import QtCore, QtGui, uic
from ConfigParser import SafeConfigParser
import math, sys
import Subsystems.Support_Files.extmath as extmath
import Subsystems.Support_Files.constants as consts
import numpy as np
from decimal import Decimal


qtCreatorLaser = "Subsystems/ui_Files/Laser_Widget.ui"
laser_widget, laserBaseClass = uic.loadUiType(qtCreatorLaser)
qtCreatorDefinedLaser = "Subsystems/ui_Files/DefinedLaser.ui"
DefinedLaserWidget, DefinedLaserBaseClass = uic.loadUiType(qtCreatorDefinedLaser)
qtCreatorUndefinedLaser = "Subsystems/ui_Files/UndefinedLaser.ui"
UndefinedLaserWidget, UndefinedLaserBaseClass = uic.loadUiType(qtCreatorUndefinedLaser)

qtCreatorNewLaser = "Subsystems/ui_Files/NewLaser.ui"
NewLaserClass, NewLaserBaseClass = uic.loadUiType(qtCreatorNewLaser)

qtCreatorRemoveLaser = "Subsystems/ui_Files/RemoveLaser.ui"
RemoveLaserClass, RemoveLaserBaseClass = uic.loadUiType(qtCreatorRemoveLaser)

qtCreatorDuplicateLaser = "Subsystems/ui_Files/DuplicateLaser.ui"
DuplicateLaserClass, DuplicateLaserBaseClass = uic.loadUiType(qtCreatorDuplicateLaser)

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
        self.min_frep = extmath.myfloat(LaserType.get('repetition rate min'))
        self.scale_frep = extmath.myfloat(LaserType.get('repetition rate max'))-self.min_frep
        self.slide_frep.setValue((self.num_frep.value()*self.pot_frep-self.min_frep)*
                self.slide_frep.maximum()/self.scale_frep)

        temp = extmath.prefixedValue(LaserType.get('pulse duration'))
        self.num_tau.display(temp[1])
        self.unit_tau.setText(temp[0]+'s')
        self.pot_tau = pow(10, temp[2])
        self.min_tau = extmath.myfloat(LaserType.get('pulse duration min'))
        self.scale_tau = extmath.myfloat(LaserType.get('pulse duration max'))-self.min_tau
        self.slide_tau.setValue((self.num_tau.value()*self.pot_tau-self.min_tau)*
                self.slide_tau.maximum()/self.scale_tau)
        
        temp = extmath.prefixedValue(LaserType.get('fire duration'))
        self.num_T.display(temp[1])
        self.unit_T.setText(temp[0]+'s')
        self.pot_T = pow(10, temp[2])
        self.min_T = extmath.myfloat(LaserType.get('fire duration min'))
        self.scale_T = extmath.myfloat(LaserType.get('fire duration max'))-self.min_T
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

    def get_duration(self):
        return self.num_T.value()*self.pot_T

################### End of Defined Laser ###########################

class UndefinedLaser(UndefinedLaserBaseClass, UndefinedLaserWidget):
    def __init__(self, main, parent=None):
        super(UndefinedLaser, self).__init__(parent)
        self.setupUi(self)
        self.main = main
        self.main.laserConf.add_section('Custom')
        if 'Custom' not in self.main.laser_type_list:
            self.main.laserType.addItem('Custom')
            self.main.laser_type_list.append('Custom')
        LT = {'Power':'1000', 'Power min':'1E+00', 'Power max':'5E+06',
              'Energy':'1E-09', 'Energy min':'1E-09', 'Energy max':'1E+00',
              'Lambda':'1E-09', 'Lambda min':'1E-09', 'Lambda max':'1E+00', 
              'M2':'1', 'M2 min':'1', 'M2 max':'1E+02',
              'Cb':'1', 'Cb min':'1', 'Cb max':'1E+01',
              'Repetition rate':'1', 'Pulse duration':'1e-09'}
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
        
        self.slide_P.sliderMoved.connect(lambda value: self.slide_moved(value, 'P'))
        self.slide_W.sliderMoved.connect(lambda value: self.slide_moved(value, 'W'))
        self.slide_lambda.sliderMoved.connect(lambda value: self.slide_moved(value, 'lambda'))
        self.slide_M2.sliderMoved.connect(lambda value: self.slide_moved(value, 'M2'))
        self.slide_Cb.sliderMoved.connect(lambda value: self.slide_moved(value, 'Cb'))
        self.slide_frep.sliderMoved.connect(lambda value: self.slide_moved(value, 'frep'))
        self.slide_tau.sliderMoved.connect(lambda value: self.slide_moved(value, 'tau'))
        self.slide_T.sliderMoved.connect(lambda value: self.slide_moved(value, 'T'))

        self.slide_P.valueChanged.connect(lambda value: self.slide_changed(value, 'P'))
        self.slide_W.valueChanged.connect(lambda value: self.slide_changed(value, 'W'))
        self.slide_lambda.valueChanged.connect(lambda value: self.slide_changed(value, 'lambda'))
        self.slide_M2.valueChanged.connect(lambda value: self.slide_changed(value, 'M2'))
        self.slide_Cb.valueChanged.connect(lambda value: self.slide_changed(value, 'Cb'))
        self.slide_frep.valueChanged.connect(lambda value: self.slide_changed(value, 'frep'))
        self.slide_tau.valueChanged.connect(lambda value: self.slide_changed(value, 'tau'))
        self.slide_T.valueChanged.connect(lambda value: self.slide_changed(value, 'T'))

        self.unit_P.activated[str].connect(lambda choice: self.unit_change(choice, 'P'))
        self.unit_W.activated[str].connect(lambda choice: self.unit_change(choice, 'W'))
        self.unit_lambda.activated[str].connect(lambda choice: self.unit_change(choice, 'lambda'))
        self.unit_frep.activated[str].connect(lambda choice: self.unit_change(choice, 'frep'))
        self.unit_tau.activated[str].connect(lambda choice: self.unit_change(choice, 'tau'))
        self.unit_T.activated[str].connect(lambda choice: self.unit_change(choice, 'T'))

    def build_unit_box(self, measure):
        listed = []
        keylist = []
        exec('mini = self.min_' + measure)
        exec('maxi = self.max_' + measure)
        for key in extmath.allPot.keys():
            pot = float(key)
            if pot > mini/1000 and pot < maxi and key not in [1e-02, 1e-01, 1e+01, 1e+02]:
                pref = extmath.allPot.get(key)
                keylist.append(float(key))
        keylist.sort()
        for key in keylist:
            listed.append(unicode(extmath.allPot.get(key) + units.get(measure)))
        exec('self.unit_'+measure+'.addItems(listed)')

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
        exec('self.min_'+SHORT+' = extmath.myfloat(self.LaserType.get(str(LONG + \' min\')))')
        exec('self.max_'+SHORT+' = extmath.myfloat(self.LaserType.get(str(LONG + \' max\')))')
        self.build_unit_box(SHORT)
        pot = pow(10, temp[2])
        exec('self.pot_' + SHORT + ' = pot')
        if pot != 1:
            self.set_unit(SHORT)
        exec('self.scale_'+SHORT+' = self.max_' + SHORT + '-self.min_' + SHORT)
        exec('self.slide_'+SHORT+'.setValue(self.num_'+SHORT+'.value())')

    def set_unit(self, var):
        exec('p = self.pot_' + var)
        power = '%.0E' % Decimal(p)
        prefixedunit = extmath.allPot.get(p) + units.get(var)
        exec('unit = self.unit_' + var)
        for ind in range(0, unit.count()):
            if unit.itemText(ind) == prefixedunit:
                unit.setCurrentIndex(ind)
                break

    def unit_change(self, choice, var):
        if var == 'frep':
            pref = unicode(choice[0:len(choice)-2])
        else:
            pref = unicode(choice[0:len(choice)-1])
        exec('old_pot = self.pot_' + var)
        new_pot = extmath.myfloat(extmath.allPrefixes.get(pref))
        exec('self.pot_' + var + ' = new_pot')
        exec('val = new_pot * self.num_'+var+'.value()')
        exec('mini = self.min_'+var)
        exec('maxi = self.max_'+var)
        if val < mini:
            exec('self.num_'+var+'.display(mini/new_pot)')
            exec('self.slide_'+var+'.setValue(mini/new_pot)')
            exec('self.main.lasersystem._' + var + '= mini')
        elif val > maxi:
            exec('self.num_'+var+'.display(maxi/new_pot)')
            exec('self.slide_'+var+'.setValue(maxi/new_pot)')
            exec('self.main.lasersystem._' + var + '= maxi')
        else:
            exec('self.main.lasersystem._' + var + '= val')

    def double_freq(self):
        if self.freqDub.isChecked():
            self.main.lasersystem.doubfreq()
        else:
            self.main.lasersystem.normfreq()

    def slide_trigged(self, action, var):
        exec('val = self.slide_' + var + '.value()')
        exec('pot = self.pot_' + var)
        exec('self.num_' + var + '.display(val)')
        if var != 'T':
            exec('self.main.lasersystem._' + var + ' = val*pot')

    def slide_moved(self, value, var):
        exec('self.num_' + var + '.display(value)')

    def slide_changed(self, value, var):
        exec('pot = self.pot_' + var)
        exec('mini = self.min_'+var)
        exec('maxi = self.max_'+var)
        if value*pot < mini:
            value = mini/pot
            exec('self.slide_'+var+'.setValue(value)')
        elif value*pot > maxi:
            value = maxi/pot
            exec('self.slide_'+var+'.setValue(value)')
        exec('self.num_' + var + '.display(value)')
        if var != 'T':
            exec('self.main.lasersystem._' + var + ' = value*pot')

    def get_duration(self):
        return self.num_T.value()*self.pot_T

#################### End of Undefined Laser ########################

class NewLaser(NewLaserBaseClass, NewLaserClass):
    def __init__(self, main, parent=None):
        super(NewLaser, self).__init__(parent)
        self.setupUi(self)
        self.main = main

        self.validname = False
        self.validP = False
        self.validW = False
        self.validlam = False
        self.validM2 = False
        self.validCb = False
        self.validfrep = False
        self.validtau = False

        self.valueW = None
        self.valuefrep = None
        
        self.P.setValidator(QtGui.QDoubleValidator())
        self.W.setValidator(QtGui.QDoubleValidator())
        self.lam.setValidator(QtGui.QDoubleValidator())
        self.M2.setValidator(QtGui.QDoubleValidator())
        self.Cb.setValidator(QtGui.QDoubleValidator())
        self.frep.setValidator(QtGui.QDoubleValidator())
        self.tau.setValidator(QtGui.QDoubleValidator())

        self.name.editingFinished.connect(self.updatename)
        self.P.editingFinished.connect(self.updateP)
        self.W.editingFinished.connect(lambda val=None:
                self.updateW(extmath.myfloat(val)))
        self.lam.editingFinished.connect(self.updatelam)
        self.M2.editingFinished.connect(self.updateM2)
        self.Cb.editingFinished.connect(self.updateCb)
        self.frep.editingFinished.connect(lambda val=None: 
                self.updatefrep(extmath.myfloat(val)))
        self.tau.editingFinished.connect(self.updatetau)

        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(False)
        self.buttonBox.accepted.connect(self.OKClicked)
#        self.buttonBox.rejected.connect(self.cancelClicked)

    def updatename(self):
        name = str(self.name.text())
        if len(str(name)) < 1:
            self.validname = False
            self.name.setText("name required")
        elif self.main.laserConf.has_section(name):
            self.validname = False
            self.name.setText("in use")
        else:
            self.validname = True
        self.checkOK()

    def updateP(self):
        P = float(self.P.text())
        if P <= 0:
            self.P.setText("value too low")
            self.validP = False
        else:
            self.valueP = P
            self.validP = True
        self.checkOK()

    def updateW(self, W):
        if W == None:
            W = extmath.myfloat(self.W.text())
        if W <= 0:
            self.W.setText("value too low")
            self.validW = False
        else:
            self.valueW = W
            self.W.setText(str(W))
            self.validW = True
            if self.validP:
                frep = self.valueP / W
                if self.valuefrep != frep:
                    self.updatefrep(frep)
        self.checkOK()

    def updatelam(self):
        lam = float(self.lam.text())
        if lam <= 0:
            self.lam.setText("value too low")
            self.validlam = False
        else:
            self.valuelam = lam
            self.validlam = True
        self.checkOK()

    def updateM2(self):
        M2 = float(self.M2.text())
        if M2 < 1:
            self.M2.setText("value too low")
            self.validM2 = False
        else:
            self.valueM2 = M2
            self.validM2 = True
        self.checkOK()

    def updateCb(self):
        Cb = float(self.Cb.text())
        if Cb < 1:
            self.Cb.setText("value too low")
            self.validCb = False
        else:
            self.valueCb = Cb
            self.validCb = True
        self.checkOK()

    def updatefrep(self, frep):
        if frep == None:
            frep = extmath.myfloat(self.frep.text())
        if frep <= 0:
            self.frep.setText("value too low")
            self.validfrep = False
        else:
            self.valuefrep = frep
            self.frep.setText(str(frep))
            self.validfrep = True
            if self.validP:
                W = self.valueP / frep
                if self.valueW != W:
                    self.updateW(W)
            if self.validtau:
                taumax = 1 / frep
                if self.valuetau > taumax:
                    self.tau.setText("max value: " + str(taumax))
                    self.validtau = False
        self.checkOK()

    def updatetau(self):
        tau = float(self.tau.text())
        if tau <= 0:
            self.tau.setText("value too low")
            self.validtau = False
        elif self.validfrep:
            taumax = 1 / self.valuefrep
            if tau > taumax:
                self.tau.setText("max value: " + str(taumax))
                self.validtau = False
            else:
                self.valuetau = tau
                self.validtau = True
        else:
            self.valuetau = tau
            self.validtau = True
        self.checkOK()

    def checkOK(self):
        if (self.validname and self.validP and self.validW and self.validlam and
            self.validM2 and self.validCb and self.validfrep and self.validtau):
            self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(False)

    def OKClicked(self):
        name = str(self.name.text())
        self.main.laserConf.add_section(name)
        self.main.laserConf.set(name, "power", str(self.valueP))
        self.main.laserConf.set(name, "energy", str(self.valueW))
        self.main.laserConf.set(name, "lambda", str(self.valuelam))
        self.main.laserConf.set(name, "m2", str(self.valueM2))
        self.main.laserConf.set(name, "cb", str(self.valueCb))
        self.main.laserConf.set(name, "repetition rate", str(self.valuefrep))
        self.main.laserConf.set(name, "tau", str(self.valuetau))
        
        if "Custom" in self.main.laser_type_list:
            pos = self.main.laserType.count()-1
        else:
            pos = self.main.laserType.count()
        self.main.laserType.insertItem(pos, name)
        self.main.laser_type_list.insert(pos, name)

######################### End of New Laser #########################

class RemoveLaser(RemoveLaserBaseClass, RemoveLaserClass):
    def __init__(self, main, parent=None):
        super(RemoveLaser, self).__init__(parent)
        self.setupUi(self)
        self.main = main

        for laser in self.main.laser_type_list:
            if laser != "Choose" and laser != "Custom":
                self.laserListWidget.addItem(laser)

        self.buttonBox.accepted.connect(self.remove)

    def remove(self):
        i = self.laserListWidget.currentRow()
        if i > -1:
            del self.main.laser_type_list[i]
            name = str(self.laserListWidget.currentItem().text())
            self.main.laserConf.remove_section(name)
            ind = self.main.laserType.findText(name)
            self.main.laserType.removeItem(ind)

skipThis = 00
renameThis = 01
replaceThis = 02
skipAll = 10
renameAll = 11
replaceAll = 12

class DuplicateLaser(DuplicateLaserBaseClass, DuplicateLaserClass):
    def __init__(self, name, parent=None):
        super(DuplicateLaser, self).__init__(parent)
        self.setupUi(self)

        self.textBox.setText("A laser with the name " + str(name) +
                " in already in use. \nWhat would you like to do?")

        self.skipButton.clicked.connect(self.skip)
        self.renameButton.clicked.connect(self.rename)
        self.replaceButton.clicked.connect(self.replace)

    def skip(self):
        if self.apply2All.isChecked():
            self.done(skipAll)
        else:
            self.done(skipThis)

    def rename(self):
        if self.apply2All.isChecked():
            self.done(renameAll)
        else:
            self.done(renameThis)

    def replace(self):
        if self.apply2All.isChecked():
            self.done(replaceAll)
        else:
            self.done(replaceThis)
