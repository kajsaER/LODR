from PyQt4 import QtCore, QtGui, uic
import math
from orbit import orbit

qtCreatorNewOrbit = "Subsystems/NewOrbit.ui"
NewOrbitClass, NewOrbitBaseClass = uic.loadUiType(qtCreatorNewOrbit)

amin = 6000
amax = 800000
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
        self.valida = False
        self.validepsilon = False
        self.validomega = False

        self.a.setValidator(QtGui.QDoubleValidator())
        self.epsilon.setValidator(QtGui.QDoubleValidator())
        self.omega.setValidator(QtGui.QDoubleValidator())

        self.name.editingFinished.connect(self.updatename)
        self.a.editingFinished.connect(self.updatea)
        self.epsilon.editingFinished.connect(self.updateepsilon)
        self.omega.editingFinished.connect(self.updateomega)

        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(False)
        self.buttonBox.accepted.connect(self.OKClicked)
        self.buttonBox.rejected.connect(self.cancelClicked)

    def updatename(self):
        if len(str(self.name)) < 1:
            self.validname = False
        if self.main.debrisConf.has_section(self.name):
            self.validname = False
            self.name.setText("in use")
        else:
            self.validname = True

    def updatea(self):
        a = float(self.a.text())
        if a >= amin and a <= amax:
            self.valuea = a
            self.valida = True
        else:
            self.a.setText("invalid")
            self.valida = False
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
        if self.valida and self.validepsilon and self.validomega:
            self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(False)

    def OKClicked(self):
        self.main.orbit_list.append(self.name.text())
        self.main.orbitConf.add_section(self.name)
        self.main.orbitConf.set(self.name, "a", str(self.valuea))
        self.main.orbitConf.set(self.name, "epsilon", str(self.valueepsilon))
        self.main.orbitConf.set(self.name, "omega", str(self.valueomega))

    def cancelClicked(self):
        print "Candeled"
