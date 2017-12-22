from PyQt4 import QtCore, QtGui, uic
import math

qtCreatorNewDebris = "Subsystems/NewDebris.ui"
NewDebrisClass, NewDebrisBaseClass = uic.loadUiType(qtCreatorNewDebris)

mmin = 0
mmax = 100
dmin = 0
dmax = 5
Cmmin = 0
Cmmax = 400
etacmin = 0
etacmax = 1
numin = 0
numax = 2*math.pi

class NewDebris(NewDebrisBaseClass, NewDebrisClass):
    def __init__(self, main, parent=None):
        super(NewDebris, self).__init__(parent)
        self.setupUi(self)
        self.main = main
        self.orbitList = []
        for orbit in self.main.orbit_list:
            self.orbitList.append(orbit)
            self.orbitListWidget.addItem(orbit)
        
        self.validm = False
        self.validd = False
        self.validCm = False
        self.validetac = False
        self.validnu = False

        self.m.setValidator(QtGui.QDoubleValidator())
        self.d.setValidator(QtGui.QDoubleValidator())
        self.Cm.setValidator(QtGui.QDoubleValidator())
        self.etac.setValidator(QtGui.QDoubleValidator())
        self.nu.setValidator(QtGui.QDoubleValidator())

        self.m.editingFinished.connect(self.updatem)
        self.d.editingFinished.connect(self.updated)
        self.Cm.editingFinished.connect(self.updateCm)
        self.etac.editingFinished.connect(self.updateetac)
        self.nu.editingFinished.connect(self.updatenu)
        self.orbitListWidget.currentRowChanged.connect(self.checkOK)
        
        self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(False)
        self.buttonBox.accepted.connect(self.OKClicked)
        self.buttonBox.rejected.connect(self.cancelClicked)
        self.newOrbitButton.clicked.connect(self.add_orbit)

    def updatem(self):
        m = float(self.m.text())
        if m > mmin and m <= mmax:
            self.valuem = m
            self.validm = True
        else:
            self.m.setText("invaild")
            self.validm = False
        self.checkOK()
    
    def updated(self):
        d = float(self.d.text())
        if d > dmin and d <= dmax:
            self.valued = d
            self.validd = True
        else:
            self.d.setText("invaild")
            self.validd = False
        self.checkOK()

    def updateCm(self):
        Cm = float(self.Cm.text())
        if Cm > Cmmin and Cm <= Cmmax:
            self.valueCm = Cm
            self.validCm = True
        else:
            self.Cm.setText("invaild")
            self.validCm = False
        self.checkOK()

    def updateetac(self):
        etac = float(self.etac.text())
        if etac > etacmin and etac <= etacmax:
            self.valueetac = etac
            self.validetac = True
        else:
            self.etac.setText("invaild")
            self.validetac = False
        self.checkOK()

    def updatenu(self):
        nu = float(self.nu.text())
        if nu > numin and nu <= numax:
            self.valuenu = nu
            self.validnu = True
        else:
            self.nu.setText("invaild")
            self.validnu = False
        self.checkOK()

    def checkOK(self):
        if (self.orbitListWidget.currentRow() > -1 and self.validm and 
                self.validd and self.validCm and
                self.validetac and self.validnu):
            self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(False)
    
    def add_orbit(self):
        self.main.add_orbit()
        for orbit in self.main.orbit_list:
            if orbit not in self.orbitList:
                self.orbitList.append(orbit)
                self.orbitListWidget.addItem(orbit)
                self.orbitListWidget.sortItems(order=QtCore.Qt.AscendingOrder)

    def OKClicked(self):
        self.main.indeb = False
        print "OK!"

    def cancelClicked(self):
        self.main.indeb = False
        print "Cancel"
