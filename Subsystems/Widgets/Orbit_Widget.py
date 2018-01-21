from PyQt4 import QtCore, QtGui, uic
import math
#from orbit import orbit

qtCreatorNewOrbit = "Subsystems/ui_Files/NewOrbit.ui"
NewOrbitClass, NewOrbitBaseClass = uic.loadUiType(qtCreatorNewOrbit)

qtCreatorRemoveOrbit = "Subsystems/ui_Files/RemoveOrbit.ui"
RemoveOrbitClass, RemoveOrbitBaseClass = uic.loadUiType(qtCreatorRemoveOrbit)

qtCreatorDuplicateOrbit = "Subsystems/ui_Files/DuplicateOrbit.ui"
DuplicateOrbitClass, DuplicateOrbitBaseClass = uic.loadUiType(qtCreatorDuplicateOrbit)

rpmin = 6538e+03 # Altitude at perigee must be at least 160 km 
rpmax = 150e+06  # Radious at perigee for a very HEO
emin = 0
emax = 1
omin = 0
omax = 2*math.pi

class NewOrbit(NewOrbitBaseClass, NewOrbitClass):
    def __init__(self, main, parent=None):
        super(NewOrbit, self).__init__(parent)
        self.setupUi(self)
        self.main = main

        self.validname = False
        self.validrp = False
        self.validepsilon = False
        self.validomega = False

        self.rp.setValidator(QtGui.QDoubleValidator())
        self.epsilon.setValidator(QtGui.QDoubleValidator())
        self.omega.setValidator(QtGui.QDoubleValidator())

        self.name.editingFinished.connect(self.updatename)
        self.rp.editingFinished.connect(self.updaterp)
        self.epsilon.editingFinished.connect(self.updateepsilon)
        self.omega.editingFinished.connect(self.updateomega)

        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(False)
        self.buttonBox.accepted.connect(self.OKClicked)
#        self.buttonBox.rejected.connect(self.cancelClicked)

    def updatename(self):
        name = str(self.name.text())
        if len(name) < 1:
            self.validname = False
            self.name.setText("name required")
        if self.main.orbitConf.has_section(name):
            self.validname = False
            self.name.setText("in use")
        else:
            self.validname = True

    def updaterp(self):
        rp = float(self.rp.text())*1e+03
        if rp >= rpmin and rp <= rpmax:
            self.valuerp = rp
            self.validrp = True
        else:
            self.rp.setText("invalid")
            self.validrp = False
        self.checkOK()

    def updateepsilon(self):
        e = float(self.epsilon.text())
        if e > emin and e < emax:
            self.valueepsilon = e
            self.validepsilon = True
        else:
            self.epsilon.setText("invalid")
            self.validepsilon = False
        self.checkOK()

    def updateomega(self):
        o = float(self.omega.text())
        if o >= omin and o < omax:
            self.valueomega = o
            self.validomega = True
        else:
            self.omega.setText("invalid")
            self.validomega = False
        self.checkOK()

    def checkOK(self):
        if self.validrp and self.validepsilon and self.validomega:
            self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(False)

    def OKClicked(self):
        name = str(self.name.text())
        self.main.orbit_list.append(name)
        self.main.orbitConf.add_section(name)
        self.main.orbitConf.set(name, "rp", str(self.valuerp))
        self.main.orbitConf.set(name, "epsilon", str(self.valueepsilon))
        self.main.orbitConf.set(name, "omega", str(self.valueomega))


class RemoveOrbit(RemoveOrbitBaseClass, RemoveOrbitClass):
    def __init__(self, main, parent=None):
        super(RemoveOrbit, self).__init__(parent)
        self.setupUi(self)
        self.main = main
        
        for orbit in self.main.orbit_list:
            self.orbitListWidget.addItem(orbit)
        
        self.buttonBox.accepted.connect(self.remove)


    def remove(self):
        i = self.orbitListWidget.currentRow()
        if i > -1:
            del self.main.orbit_list[i]
            name = str(self.orbitListWidget.currentItem().text())
            self.main.orbitConf.remove_section(name)

skipThis = 00
renameThis = 01
replaceThis = 02
skipAll = 10
renameAll = 11
replaceAll = 12

class DuplicateOrbit(DuplicateOrbitBaseClass, DuplicateOrbitClass):
    def __init__(self, name, parent=None):
        super(DuplicateOrbit, self).__init__(parent)
        self.setupUi(self)

        self.textBox.setText("An orbit with the name " + str(name) +
                " is already in use. \nWhat would you like to do?")

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

