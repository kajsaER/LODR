from PyQt5 import QtCore, QtWidgets, QtGui, uic
import math

qtCreatorNewOrbit = "Subsystems/ui_Files/NewOrbit.ui"
NewOrbitClass, NewOrbitBaseClass = uic.loadUiType(qtCreatorNewOrbit)

qtCreatorRemoveOrbit = "Subsystems/ui_Files/RemoveOrbit.ui"
RemoveOrbitClass, RemoveOrbitBaseClass = uic.loadUiType(qtCreatorRemoveOrbit)

qtCreatorDuplicateOrbit = "Subsystems/ui_Files/DuplicateOrbit.ui"
DuplicateOrbitClass, DuplicateOrbitBaseClass = uic.loadUiType(qtCreatorDuplicateOrbit)

rpmin = 6538e+03    # Altitude at perigee must be at least 160 km 
rpmax = 150e+06     # Radious at perigee for a very HEO
emin = 0            # Minimum eccentricity
emax = 1            # Maximum eccentricity
omin = 0            # Minimum argument of perigee
omax = 2*math.pi    # Maximum argument of perigee

class NewOrbit(NewOrbitBaseClass, NewOrbitClass):   # Widget for making a new orbit
    def __init__(self, main, parent=None):
        super(NewOrbit, self).__init__(parent)
        self.setupUi(self)
        self.main = main

        self.validname = False
        self.validrp = False
        self.validepsilon = False
        self.validomega = False

        self.rp.setValidator(QtGui.QDoubleValidator())  # Require values to be double()
        self.epsilon.setValidator(QtGui.QDoubleValidator())
        self.omega.setValidator(QtGui.QDoubleValidator())

        # Setup feilds, buttons and connected actions
        self.name.editingFinished.connect(self.updatename)
        self.rp.editingFinished.connect(self.updaterp)
        self.epsilon.editingFinished.connect(self.updateepsilon)
        self.omega.editingFinished.connect(self.updateomega)

        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
        self.buttonBox.accepted.connect(self.OKClicked)

    def updatename(self):   # When name is edited
        name = str(self.name.text())    # Get name
        if len(name) < 1:               # If name doesn't exist
            self.validname = False      # Not valid
            self.name.setText("name required")
        elif self.main.orbitConf.has_section(name): # If name isn't unique
            self.validname = False      # Not valid
            self.name.setText("name in use")
        else:                           # Else, OK
            self.validname = True
        self.checkOK()      # Check if all is ok

    def updaterp(self):     # When rp is edited
        rp = float(self.rp.text())*1e+03    # Get rp
        if rp >= rpmin and rp <= rpmax: # If in range
            self.valuerp = rp           # Store value
            self.validrp = True         # OK
        else:                           # Else, not OK
            self.rp.setText("invalid")
            self.validrp = False
        self.checkOK()      # Check if all is ok

    def updateepsilon(self):# When ε is edited
        e = float(self.epsilon.text())  # Get ε
        if e > emin and e < emax:       # If in range
            self.valueepsilon = e       # Store value
            self.validepsilon = True    # OK
        else:                           # Else, not OK
            self.epsilon.setText("invalid")
            self.validepsilon = False
        self.checkOK()      # Check if all is ok

    def updateomega(self):  # When ω is changed
        o = float(self.omega.text())    # Get ω
        if o >= omin and o < omax:      # If in range
            self.valueomega = o         # Store value
            self.validomega = True      # OK
        else:                           # Else, not OK
            self.omega.setText("invalid")
            self.validomega = False
        self.checkOK()      # Check if all is OK

    def checkOK(self):  # Check if all values are OK, enable/disable OK button
        if self.validname and self.validrp and self.validepsilon and self.validomega:
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)

    def OKClicked(self):    # When OK button is pressed
        name = str(self.name.text())    # Get the name
        self.main.orbit_list.append(name)       # Store name in main list
        self.main.orbitConf.add_section(name)   # Make section in main Conf and store values
        self.main.orbitConf.set(name, "rp", str(self.valuerp))
        self.main.orbitConf.set(name, "epsilon", str(self.valueepsilon))
        self.main.orbitConf.set(name, "omega", str(self.valueomega))


class RemoveOrbit(RemoveOrbitBaseClass, RemoveOrbitClass):  # Widget for removing orbit
    def __init__(self, main, parent=None):
        super(RemoveOrbit, self).__init__(parent)
        self.setupUi(self)
        self.main = main
        
        for orbit in self.main.orbit_list:  # Add all available orbits in local list
            self.orbitListWidget.addItem(orbit)
        
        # Setup button and connect action
        self.buttonBox.accepted.connect(self.remove)


    def remove(self):   # When button is pushed
        i = self.orbitListWidget.currentRow()   # Get index of chosen orbit
        if i > -1:                              # If valid orbit
            del self.main.orbit_list[i]         # Delete from main list
            name = str(self.orbitListWidget.currentItem().text())   # Get name
            self.main.orbitConf.remove_section(name)    # Remove section from main Conf

# Define standard states
skipThis = 00           # Skip only current item
renameThis = 0o1        # Rename only current item
replaceThis = 0o2       # Replace only current item
skipAll = 10            # Skip all items
renameAll = 11          # Rename all items
replaceAll = 12         # Replace all items

class DuplicateOrbit(DuplicateOrbitBaseClass, DuplicateOrbitClass): # Widget for handeling duplicate entries
    def __init__(self, name, parent=None):
        super(DuplicateOrbit, self).__init__(parent)
        self.setupUi(self)
        
        # Setup message text and buttons with actions
        self.textBox.setText("An orbit with the name " + str(name) +
                " is already in use. \nWhat would you like to do?")

        self.skipButton.clicked.connect(self.skip)
        self.renameButton.clicked.connect(self.rename)
        self.replaceButton.clicked.connect(self.replace)

    def skip(self):     # When skip is pushed
        if self.apply2All.isChecked():  # Check if apply to all box is cheched
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


class NoMatch(QtWidgets.QMessageBox):   # Widget for handeling the case when no mathing orbit is found
    def __init__(self, name, parent=None):
        super(NoMatch, self).__init__(parent)

        # Setup the ui with title, text, icon and buttons
        self.setWindowTitle("No Matching Orbit Found")
        self.setText("No orbit with parameters matching the ones defined as " + repr(name) +
                     "\nfor this piece of debris.\n\nWould you like to use the parameters of the " + 
                     "stored orbit with the same name or rename the one with the specific parameters?")
        self.setIcon(QtWidgets.QMessageBox.Question)
        self.StoredBtn = self.addButton("Stored", QtWidgets.QMessageBox.RejectRole)
        self.RenameBtn = self.addButton("Rename", QtWidgets.QMessageBox.ActionRole)

        # Connect buttons to return action and exit widget
        self.StoredBtn.clicked.connect(lambda: self.done(QtWidgets.QMessageBox.RejectRole))
        self.RenameBtn.clicked.connect(lambda: self.done(QtWidgets.QMessageBox.ActionRole))
