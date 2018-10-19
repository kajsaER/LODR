from PyQt5 import QtCore, QtWidgets, QtGui, uic
from configparser import SafeConfigParser
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
counterParam = {'P':'W', 'W':'tau', }


###################### End of Preface ##############################
####################################################################
####################################################################
####################################################################
################## Beginning Defined Laser #########################


class Laser_Widget(laserBaseClass, laser_widget):   # Empty laser widget
    def __init__(self, main, parent=None):
        super(Laser_Widget, self).__init__(parent)
        self.setupUi(self)
        self.main = main


class DefinedLaser(DefinedLaserBaseClass, DefinedLaserWidget):  # Widget for predefined lasers
    def __init__(self, main, parent=None):
        super(DefinedLaser, self).__init__(parent)
        self.setupUi(self)
        self.main = main
        
        # Setup buttons, sliders and actions connected to them
        self.freqDub.toggled.connect(self.double_freq)
        self.lambda_coeff = 1
        
        self.slide_W.actionTriggered.connect(lambda act: self.slide_trigged(act, 'W'))
        self.slide_M2.actionTriggered.connect(lambda act: self.slide_trigged(act, 'M2'))
        self.slide_Cd.actionTriggered.connect(lambda act: self.slide_trigged(act, 'Cd'))
        self.slide_frep.actionTriggered.connect(lambda act: self.slide_trigged(act, 'frep'))
        self.slide_tau.actionTriggered.connect(lambda act: self.slide_trigged(act, 'tau'))
        self.slide_T.actionTriggered.connect(lambda act: self.slide_trigged(act, 'T'))

        self.slide_W.sliderMoved.connect(lambda value: self.slide_moved(value, 'W'))
        self.slide_M2.sliderMoved.connect(lambda value: self.slide_moved(value, 'M2'))
        self.slide_Cd.sliderMoved.connect(lambda value: self.slide_moved(value, 'Cd'))
        self.slide_frep.sliderMoved.connect(lambda value: self.slide_moved(value, 'frep'))
        self.slide_tau.sliderMoved.connect(lambda value: self.slide_moved(value, 'tau'))
        self.slide_T.sliderMoved.connect(lambda value: self.slide_moved(value, 'T'))

        self.slide_W.valueChanged.connect(lambda value: self.slide_changed(value, 'W'))
        self.slide_M2.valueChanged.connect(lambda value: self.slide_changed(value, 'M2'))
        self.slide_Cd.valueChanged.connect(lambda value: self.slide_changed(value, 'Cd'))
        self.slide_frep.valueChanged.connect(lambda value: self.slide_changed(value, 'frep'))
        self.slide_tau.valueChanged.connect(lambda value: self.slide_changed(value, 'tau'))
        self.slide_T.valueChanged.connect(lambda value: self.slide_changed(value, 'T'))


    def setDefaultLaserParam(self, LaserType):  # Set values to defaults for given laser type
        self.freqDub.setChecked(False)
        self.lambda_coeff = 1
        self.LaserType = LaserType

        temp = extmath.prefixedValue(LaserType.get('power'))    # Get prefixed value
        self.num_P.display(temp[1])     # Display value
        self.unit_P.setText(temp[0]+'W')# Display prefixed unit

        self.set_default_value('energy', 'W')

        temp = extmath.prefixedValue(LaserType.get('lambda'))
        self.num_lambda.display(temp[1])
        self.unit_lambda.setText(temp[0]+'m')

        self.set_default_value('m2', 'M2')
        self.set_default_value('cd', 'Cd')
        self.set_default_value('repetition rate', 'frep')
        self.set_default_value('pulse duration', 'tau')
        self.set_default_value('fire duration', 'T')

    def set_default_value(self, LONG, SHORT):   # Set default value with prefixed units
        temp = extmath.prefixedValue(self.LaserType.get(LONG))  # Get prefixed value
        exec('self.num_' + SHORT + '.display(temp[1])') # Display value
        exec('self.min_'+SHORT+' = extmath.myfloat(self.LaserType.get(str(LONG + \' min\')))')  # Get min and max values
        exec('self.max_'+SHORT+' = extmath.myfloat(self.LaserType.get(str(LONG + \' max\')))')
        pot = pow(10, temp[2])      # Get the power of 10
        exec('self.scale_'+SHORT+' = (self.max_' + SHORT + '-self.min_' + SHORT+')/'+   # Get scale for the slider
                '(self.slide_'+SHORT+'.maximum() - self.slide_'+SHORT+'.minimum())')
        if SHORT not in {'M2', 'Cd'}:   # If a power of 10 could be present
            exec('self.pot_' + SHORT + ' = pot')    # Set power of 10
            if pot != 1:            # If power of 10 isn't 1
                exec('self.unit_' + SHORT + '.setText(temp[0]+units.get(SHORT))')   # Display prefixed unit
            exec('self.slide_'+SHORT+'.setValue('+  # Move slider to the right value
                    '(self.num_'+SHORT+'.value()*self.pot_'+SHORT+'-self.min_'+SHORT+')/'+
                    'self.scale_'+SHORT+'+self.slide_'+SHORT+'.minimum())')
        else:       # If no power of 10 possible, move slider to the right value
            exec('self.slide_'+SHORT+'.setValue((self.num_'+SHORT+'.value()-self.min_'+SHORT+')/'+
                    'self.scale_'+SHORT+'+self.slide_'+SHORT+'.minimum())')
    
    def double_freq(self):  # Double or normal frequency
        if self.freqDub.isChecked():    # If doubling was ticked
            self.main.lasersystem.doubfreq()    # Set double frequency in laser
            self.lambda_coeff = 0.5     # Set λ coefficient to 0.5
            self.num_lambda.display(0.5*self.num_lambda.value())    # Display 0.5*λ
        else:                           # If doubling was unticked
            self.main.lasersystem.normfreq()    # Set normal frequency in laser
            self.lambda_coeff = 1       # Set λ coefficient to 1
            self.num_lambda.display(2*self.num_lambda.value())      # Display 2*λ

    def slide_trigged(self, action, var):   # If slider was triggered, Update value and unit
        val = eval('(self.slide_'+var+'.value()-self.slide_'+var+'.minimum())*self.scale_'+var+
                '+self.min_'+var)
        temp = extmath.prefixedValue(val)
        if var not in {'M2', 'Cd'}:
            exec('self.unit_' + var + '.setText(temp[0] + units.get(var))')
            exec('self.pot_' + var + ' = pow(10, temp[2])')
        exec('self.num_' + var + '.display(temp[1])')
        if var != 'T':          # If not fireing period, set value in laser
            exec('self.main.lasersystem._' + var + ' = val')

    def slide_moved(self, value, var):      # If slider was moved, update value and unit
        val = eval('(value-self.slide_'+var+'.minimum())*self.scale_' + var +
                '+self.min_'+var) 
        temp = extmath.prefixedValue(val)
        if var not in {'M2', 'Cd'}:
            exec('self.unit_' + var + '.setText(temp[0] + units.get(var))')
            exec('self.pot_' + var + ' = pow(10, temp[2])')
        exec('self.num_' + var + '.display(temp[1])')

    def slide_changed(self, value, var):    # If slider was changed, update value and unit
        val = eval('(value-self.slide_'+var+'.minimum())*self.scale_' + var +
                '+self.min_'+var)
        temp = extmath.prefixedValue(val)
        if var not in {'M2', 'Cd'}:
            exec('self.unit_' + var + '.setText(temp[0] + units.get(var))')
            exec('self.pot_' + var + ' = pow(10, temp[2])')
        exec('self.num_' + var + '.display(temp[1])')
        if var != 'T':          # If not fireing period, set value in laser
            exec("%s" % 'self.main.lasersystem._' + var + ' = val')

    def get_duration(self):     # Return the fireing duration 
        return self.num_T.value()*self.pot_T

################### End of Defined Laser ###########################
####################################################################
####################################################################
####################################################################
################ Beginning Undefined Laser #########################

class UndefinedLaser(UndefinedLaserBaseClass, UndefinedLaserWidget):    # Widget for free tuned lasers
    def __init__(self, main, parent=None):
        super(UndefinedLaser, self).__init__(parent)
        self.setupUi(self)
        self.main = main
        self.main.laserConf.add_section('Custom')   # Make sure laser is in main list and Conf
        if 'Custom' not in self.main.laser_type_list:
            self.main.laserType.addItem('Custom')
            self.main.laser_type_list.append('Custom')
        LT = {'Power':'1000', 'Power min':'1E+00', 'Power max':'5E+06',
              'Energy':'1E-09', 'Energy min':'1E-09', 'Energy max':'1E+00',
              'Lambda':'1E-09', 'Lambda min':'1E-09', 'Lambda max':'1E+00', 
              'M2':'1', 'M2 min':'1', 'M2 max':'1E+02',
              'Cd':'1', 'Cd min':'1', 'Cb max':'1E+01',
              'Repetition rate':'1E+11', 'Pulse duration':'1e-09'}
        for name in list(LT.keys()):
            self.main.laserConf.set('Custom', name, LT[name])

        # Setup buttons, sliders and the actions connected to them
        self.freqDub.toggled.connect(self.double_freq)
        self.lambda_coeff = 1
        
        self.slide_P.actionTriggered.connect(lambda act: self.slide_trigged(act, 'P'))
        self.slide_W.actionTriggered.connect(lambda act: self.slide_trigged(act, 'W'))
        self.slide_lambda.actionTriggered.connect(lambda act: self.slide_trigged(act, 'lambda'))
        self.slide_M2.actionTriggered.connect(lambda act: self.slide_trigged(act, 'M2'))
        self.slide_Cd.actionTriggered.connect(lambda act: self.slide_trigged(act, 'Cd'))
        self.slide_frep.actionTriggered.connect(lambda act: self.slide_trigged(act, 'frep'))
        self.slide_tau.actionTriggered.connect(lambda act: self.slide_trigged(act, 'tau'))
        self.slide_T.actionTriggered.connect(lambda act: self.slide_trigged(act, 'T'))
        
        self.slide_P.sliderMoved.connect(lambda value: self.slide_moved(value, 'P'))
        self.slide_W.sliderMoved.connect(lambda value: self.slide_moved(value, 'W'))
        self.slide_lambda.sliderMoved.connect(lambda value: self.slide_moved(value, 'lambda'))
        self.slide_M2.sliderMoved.connect(lambda value: self.slide_moved(value, 'M2'))
        self.slide_Cd.sliderMoved.connect(lambda value: self.slide_moved(value, 'Cd'))
        self.slide_frep.sliderMoved.connect(lambda value: self.slide_moved(value, 'frep'))
        self.slide_tau.sliderMoved.connect(lambda value: self.slide_moved(value, 'tau'))
        self.slide_T.sliderMoved.connect(lambda value: self.slide_moved(value, 'T'))

        self.slide_P.valueChanged.connect(lambda value: self.slide_changed(value, 'P'))
        self.slide_W.valueChanged.connect(lambda value: self.slide_changed(value, 'W'))
        self.slide_lambda.valueChanged.connect(lambda value: self.slide_changed(value, 'lambda'))
        self.slide_M2.valueChanged.connect(lambda value: self.slide_changed(value, 'M2'))
        self.slide_Cd.valueChanged.connect(lambda value: self.slide_changed(value, 'Cd'))
        self.slide_frep.valueChanged.connect(lambda value: self.slide_changed(value, 'frep'))
        self.slide_tau.valueChanged.connect(lambda value: self.slide_changed(value, 'tau'))
        self.slide_T.valueChanged.connect(lambda value: self.slide_changed(value, 'T'))

        self.unit_P.activated[str].connect(lambda choice: self.unit_change(choice, 'P'))
        self.unit_W.activated[str].connect(lambda choice: self.unit_change(choice, 'W'))
        self.unit_lambda.activated[str].connect(lambda choice: self.unit_change(choice, 'lambda'))
        self.unit_frep.activated[str].connect(lambda choice: self.unit_change(choice, 'frep'))
        self.unit_tau.activated[str].connect(lambda choice: self.unit_change(choice, 'tau'))
        self.unit_T.activated[str].connect(lambda choice: self.unit_change(choice, 'T'))

    def build_unit_box(self, measure):  # Make unit choice box
        listed = []     
        keylist = []
        mini = eval('self.min_' + measure)  # Get minimum value
        maxi = eval('self.max_' + measure)  # Get maximum value
        for key in list(extmath.allPot.keys()): # Go through all prefixes
            pot = float(key)        # Get the power of 10 for the prefix
            if pot > mini/1000 and pot < maxi and key not in [1e-02, 1e-01, 1e+01, 1e+02]:  # If pot in range
#                pref = extmath.allPot.get(key)  # Get the prefix
                keylist.append(float(key))      # Add pot to the keylist
        keylist.sort()      # Sort keylist
        for key in keylist: # Add prefixed unit for all pots to the list
            listed.append(str(extmath.allPot.get(key) + units.get(measure)))
        exec('self.unit_'+measure+'.addItems(listed)')  # Add list to choice box

    def setDefaultLaserParam(self, LaserType):  # Setup default parameters
        self.freqDub.setChecked(False)
        self.lambda_coeff = 1
        self.LaserType = LaserType

        self.set_default_value('power', 'P')
        self.set_default_value('energy', 'W')
        self.set_default_value('lambda', 'lambda')
        self.set_default_value('m2', 'M2')
        self.set_default_value('cd', 'Cd')

        self.set_default_value('repetition rate', 'frep')
        self.set_default_value('pulse duration', 'tau')
        self.set_default_value('fire duration', 'T')

    def set_default_value(self, LONG, SHORT):   # Display default values with prefixed units
        temp = extmath.prefixedValue(self.LaserType.get(LONG))  # Get prefixed values
        exec('self.num_' + SHORT + '.display(temp[1])')     # Display value
        exec('self.min_'+SHORT+' = extmath.myfloat(self.LaserType.get(str(LONG + \' min\')))')  # Get min and max
        exec('self.max_'+SHORT+' = extmath.myfloat(self.LaserType.get(str(LONG + \' max\')))')
        pot = pow(10, temp[2])      # Get power of 10
        exec('self.scale_'+SHORT+' = self.max_' + SHORT + '-self.min_' + SHORT) # Calculate scale
        if SHORT not in {'M2', 'Cd'}:   # If variable could have a pot
            exec('self.pot_' + SHORT + ' = pot')    # Set pot
            self.build_unit_box(SHORT)  # Build unit box for variable
            if pot != 1:        # If unit has prefix 
                self.set_unit(SHORT)    # Set the prefix
            exec('self.slide_'+SHORT+'.setValue(self.num_'+SHORT+'.value())')   # Set slider value
        else:                           # If variable can't have a pot, set slider value with scale
            exec('self.slide_'+SHORT+'.setValue((self.num_'+SHORT+'.value()-self.min_'+SHORT+')*'
                'self.slide_'+SHORT+'.maximum()/self.scale_'+SHORT+')')

    def set_unit(self, var):    # Set unit choice box to correct prefix
        p = eval('self.pot_' + var) # Get pot
        power = '%.0E' % Decimal(p) # Convert to scientific notation
        prefixedunit = extmath.allPot.get(p) + units.get(var)   # Get the prefixed unit for comparison
        unit = eval('self.unit_' + var) # Get unit choice box
        for ind in range(0, unit.count()):  # For all elements in choice box
            if unit.itemText(ind) == prefixedunit:  # Check if thay match with prefixed unit
                unit.setCurrentIndex(ind)           # Display right prefixed unit
                break

    def unit_change(self, choice, var):     # Unit box changed
        if var == 'frep':       # If 2 letter unit 
            pref = str(choice[0:len(choice)-2]) # Get prefix
        else:                   # If 1 letter unit
            pref = str(choice[0:len(choice)-1]) # Get prefix
        new_pot = extmath.myfloat(extmath.allPrefixes.get(pref))# Get new pot
        exec('self.pot_' + var + ' = new_pot')  # Set new pot
        val = eval('new_pot * self.num_'+var+'.value()')    # New unprefixed value
        mini = eval('self.min_'+var)            # Get min and max values
        maxi = eval('self.max_'+var)
        if val < mini:          # If value too small, adjust
            exec('self.num_'+var+'.display(mini/new_pot)')
            exec('self.slide_'+var+'.setValue(mini/new_pot)')
            exec('self.main.lasersystem._' + var + '= mini')
        elif val > maxi:        # If value too large, adjust
            exec('self.num_'+var+'.display(maxi/new_pot)')
            exec('self.slide_'+var+'.setValue(maxi/new_pot)')
            exec('self.main.lasersystem._' + var + '= maxi')
        else:                   # Set in main laser
            exec('self.main.lasersystem._' + var + '= val')

    def double_freq(self):      # Double or normal frequency
        if self.freqDub.isChecked():    # If doubling is ticked
            self.main.lasersystem.doubfreq()    # Set doubling in main laser
            self.lambda_coeff = 0.5     # Set λ ceofficient to 0.5
            self.num_lambda.display(0.5*self.num_lambda.value())    # Set 0.5*λ
        else:                           # If doubling is unticked
            self.main.lasersystem.normfreq()    # Set normal in main laser
            self.lambda_coeff = 1       # Set λ coefficient to 1
            self.num_lambda.display(2*self.num_lambda.value())      # Set 2*λ

    def slide_trigged(self, action, var):   # If slider was trigged, update value and unit
        if var not in {'M2', 'Cd'}:
            val = eval('self.slide_' + var + '.value()')
            pot = eval('self.pot_' + var)
        else:
            val = eval('self.slide_' + var + '.value()*self.scale_'+
                  var + '/self.slide_' + var + '.maximum() + self.min_' + var)
            pot = 1
        exec('self.num_' + var + '.display(val)')
        if var != 'T':
            exec('self.main.lasersystem._' + var + ' = val*pot')

    def slide_moved(self, value, var):      # If slider was moved, update value and unit 
        if var not in {'M2', 'Cd'}:
            val = value
        else:
            val = eval('value*self.scale_' + var +
                '/self.slide_' + var + '.maximum() + self.min_' + var)
        exec('self.num_' + var + '.display(val)')

    def slide_changed(self, value, var):    # If slider was changed, update value and unit
        if var not in {'M2', 'Cd'}:
            val = value
            pot = eval('self.pot_' + var)
        else:
            val = eval('value*self.scale_' + var +
                '/self.slide_' + var + '.maximum() + self.min_' + var)
            pot = 1
        exec('self.num_' + var + '.display(val)')
        if var != 'T':
            exec('self.main.lasersystem._' + var + ' = val*pot')

    def get_duration(self): # Return fireing duration
        return self.num_T.value()*self.pot_T

#################### End of Undefined Laser ########################
####################################################################
####################################################################
####################################################################
####################################################################

class NewLaser(NewLaserBaseClass, NewLaserClass):   # Widget for making new defined lasers
    def __init__(self, main, parent=None):
        super(NewLaser, self).__init__(parent)
        self.setupUi(self)
        self.main = main

        self.validname = False
        self.validP = False
        self.validW = False
        self.validlam = False
        self.validM2 = False
        self.validCd = False
        self.validfrep = False
        self.validtau = False

        self.valueW = None
        self.valuefrep = None
        
        self.P.setValidator(QtGui.QDoubleValidator())   # Require double values
        self.W.setValidator(QtGui.QDoubleValidator())
        self.lam.setValidator(QtGui.QDoubleValidator())
        self.M2.setValidator(QtGui.QDoubleValidator())
        self.Cd.setValidator(QtGui.QDoubleValidator())
        self.frep.setValidator(QtGui.QDoubleValidator())
        self.tau.setValidator(QtGui.QDoubleValidator())

        # Connect feilds to actions
        self.name.editingFinished.connect(self.updatename)
        self.P.editingFinished.connect(self.updateP)
        self.W.editingFinished.connect(lambda val=None:
                self.updateW(extmath.myfloat(val)))
        self.lam.editingFinished.connect(self.updatelam)
        self.M2.editingFinished.connect(self.updateM2)
        self.Cd.editingFinished.connect(self.updateCd)
        self.frep.editingFinished.connect(lambda val=None: 
                self.updatefrep(extmath.myfloat(val)))
        self.tau.editingFinished.connect(self.updatetau)

        # Setup buttons and actions
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
        self.buttonBox.accepted.connect(self.OKClicked)

    def updatename(self):   # Check if name is valid and unique
        name = str(self.name.text())
        if len(str(name)) < 1:
            self.validname = False
            self.name.setText("name required")
        elif self.main.laserConf.has_section(name):
            self.validname = False
            self.name.setText("in use")
        else:
            self.validname = True
        self.checkOK()      # Check if ready to save

    def updateP(self):      # Check if power is positive
        P = float(self.P.text())
        if P <= 0:
            self.P.setText("value too low")
            self.validP = False
        else:
            self.valueP = P
            self.validP = True
        self.checkOK()      # Check if ready to save

    def updateW(self, W):   # Check if energy is OK
        if W == None:       # If no new value was given
            W = extmath.myfloat(self.W.text()) # Get value
        if W <= 0:          # If negative, not ok
            self.W.setText("value too low")
            self.validW = False
        else:               # If positive
            self.valueW = W # Store value 
            self.W.setText(str(W))  # Set value
            self.validW = True  # Set valid
            if self.validP:     # If valid power
                frep = self.valueP / W  # Get associated frep
                if self.valuefrep != frep:  # Make sure frep is right
                    self.updatefrep(frep)
        self.checkOK()      # Check if ready to save

    def updatelam(self):    # Check if λ is ok
        lam = float(self.lam.text())
        if lam <= 0:
            self.lam.setText("value too low")
            self.validlam = False
        else:
            self.valuelam = lam
            self.validlam = True
        self.checkOK()      # Check if ready to save

    def updateM2(self):     # Check if M² if ok
        M2 = float(self.M2.text())
        if M2 < 1:
            self.M2.setText("value too low")
            self.validM2 = False
        else:
            self.valueM2 = M2
            self.validM2 = True
        self.checkOK()      # Check if ready to save

    def updateCd(self):     # Check if Cd is ok
        Cd = float(self.Cd.text())
        if Cd < 1:
            self.Cd.setText("value too low")
            self.validCd = False
        else:
            self.valueCd = Cd
            self.validCd = True
        self.checkOK()      #Check if ready to save

    def updatefrep(self, frep): # Check if frep is ok
        if frep == None:    # If no value was given
            frep = extmath.myfloat(self.frep.text())    # Get value
        if frep <= 0:       # If negative, not ok
            self.frep.setText("value too low")
            self.validfrep = False
        else:               # If positive
            self.valuefrep = frep   # Set value
            self.frep.setText(str(frep))    # Display value
            self.validfrep = True
            if self.validP: # If power is valid
                W = self.valueP / frep  # Get correct W
                if self.valueW != W:    # Make sure right W
                    self.updateW(W)
            if self.validtau:   # If τ is valid
                taumax = 1 / frep   # Get maximum τ
                if self.valuetau > taumax:  # If τ is too large, not ok
                    self.tau.setText("max value: " + str(taumax))
                    self.validtau = False
        self.checkOK()      # Check if ready to save

    def updatetau(self):    # Check if τ is ok
        tau = float(self.tau.text())    # Get value
        if tau <= 0:        # If negative, not ok
            self.tau.setText("value too low")
            self.validtau = False
        elif self.validfrep:    # If frep is ok
            taumax = 1 / self.valuefrep # Compute maximum τ
            if tau > taumax:    # If τ is too big, not ok
                self.tau.setText("max value: " + str(taumax))
                self.validtau = False
            else:               # If τ is ok, then it's ok
                self.valuetau = tau
                self.validtau = True
        else:               # If no frep, then τ is ok
            self.valuetau = tau
            self.validtau = True
        self.checkOK()      # Check if ready to save

    def checkOK(self):      # Check if all values are valid, if so enable ok button
        if (self.validname and self.validP and self.validW and self.validlam and
            self.validM2 and self.validCd and self.validfrep and self.validtau):
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)
        else:               # If not, diable ok button
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)

    def OKClicked(self):    # When ok is clicked, save data
        name = str(self.name.text())
        self.main.laserConf.add_section(name)   # Add a new section to the main conf
        self.main.laserConf.set(name, "power", str(self.valueP))
        self.main.laserConf.set(name, "energy", str(self.valueW))
        self.main.laserConf.set(name, "lambda", str(self.valuelam))
        self.main.laserConf.set(name, "m2", str(self.valueM2))
        self.main.laserConf.set(name, "cd", str(self.valueCd))
        self.main.laserConf.set(name, "repetition rate", str(self.valuefrep))
        self.main.laserConf.set(name, "tau", str(self.valuetau))
        
        if "Custom" in self.main.laser_type_list:   # If main list includes "Custom"
            pos = self.main.laserType.count()-1     # Put second last in list
        else:                                       # If no "Custom"
            pos = self.main.laserType.count()       # Put last in the list
        self.main.laserType.insertItem(pos, name)
        self.main.laser_type_list.insert(pos, name)

######################### End of New Laser #########################

class RemoveLaser(RemoveLaserBaseClass, RemoveLaserClass):  # Widget for removing laser
    def __init__(self, main, parent=None):
        super(RemoveLaser, self).__init__(parent)
        self.setupUi(self)
        self.main = main

        for laser in self.main.laser_type_list: # For all items in the list
            if laser != "Choose" and laser != "Custom": # Except Choose and Custom
                self.laserListWidget.addItem(laser) # Put in a new list

        # Setup and connect button and action
        self.buttonBox.accepted.connect(self.remove)

    def remove(self):   # When button has been pushed
        i = self.laserListWidget.currentRow()   # Get current index in the laser list
        if i > -1:      # If valid index
            del self.main.laser_type_list[i]    # Delete from main list
            name = str(self.laserListWidget.currentItem().text())   # Get name of the laser
            self.main.laserConf.remove_section(name)    # Remove named section from Conf
            ind = self.main.laserType.findText(name)    # Get index in main list
            self.main.laserType.removeItem(ind)         # Remove said item

# Define standard states
skipThis = 00       # Skip only current item
renameThis = 0o1    # Rename only current item
replaceThis = 0o2   # Replace only current item
skipAll = 10        # Skip all items
renameAll = 11      # Rename all items
replaceAll = 12     # Replace all items

class DuplicateLaser(DuplicateLaserBaseClass, DuplicateLaserClass): # Widget for handeling duplicate entries
    def __init__(self, name, parent=None):
        super(DuplicateLaser, self).__init__(parent)
        self.setupUi(self)
        
        # Setup message text and buttons with actions
        self.textBox.setText("A laser with the name " + str(name) +
                " in already in use. \nWhat would you like to do?")

        self.skipButton.clicked.connect(self.skip)
        self.renameButton.clicked.connect(self.rename)
        self.replaceButton.clicked.connect(self.replace)

    def skip(self): # When skip is pushed
        if self.apply2All.isChecked():  # Check if apply to all box is checked
            self.done(skipAll)          # If so, return skipAll value
        else:
            self.done(skipThis)         # If not, return skipThis value

    def rename(self):   # When rename is pushed
        if self.apply2All.isChecked():  # Check if apply to all box is checked
            self.done(renameAll)        # If so, return renameAll value
        else:
            self.done(renameThis)       # If not, return renameThis value

    def replace(self):  # When replace is pushed
        if self.apply2All.isChecked():  # Check if apply to all box is checked
            self.done(replaceAll)       # If so, return replaceAll value
        else:
            self.done(replaceThis)      # If not, return replaceThis value
