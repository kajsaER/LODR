from PyQt4 import QtCore, QtGui, uic
import math
from Subsystems.orbit import orbit
from Subsystems.debris import debris

qtCreatorNewDebris = "Subsystems/ui_Files/NewDebris.ui"
NewDebrisClass, NewDebrisBaseClass = uic.loadUiType(qtCreatorNewDebris)

qtCreatorRemoveDebris = "Subsystems/ui_Files/RemoveDebris.ui"
RemoveDebrisClass, RemoveDebrisBaseClass = uic.loadUiType(qtCreatorRemoveDebris)

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
#        self.buttonBox.rejected.connect(self.cancelClicked)
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
        orbname = str(self.orbitListWidget.currentItem().text())
        name = (str(hex(int(self.valuem + self.valued + 
                self.valueCm*self.valueetac + 360/math.pi*self.valuenu))) + orbname)
        extra = 0
        n0 = name
        while self.main.debrisConf.has_section(name):
            name = n0 + str(extra)
            extra += 1
        orbvals = self.main.orbitConf.items(orbname)
        self.main.debrisConf.add_section(name)
        self.main.debrisConf.set(name, "mass", str(self.valuem))
        self.main.debrisConf.set(name, "size", str(self.valued))
        self.main.debrisConf.set(name, "Cm", str(self.valueCm))
        self.main.debrisConf.set(name, "etac", str(self.valueetac))
        self.main.debrisConf.set(name, "nu", str(self.valuenu))
        self.main.debrisConf.set(name, "orbit", orbname)
        self.main.debrisConf.set("ORBITS", orbname, str(orbvals))

        orb = orbit()
        o = dict(orbvals)
        orb.make(float(o.get("rp")), float(o.get("epsilon")), float(o.get("omega")))
        deb = debris(name, self.valueetac, self.valueCm, self.valued, self.valuem, orb, self.valuenu)
        self.main.debris_list.append(deb)



class RemoveDebris(RemoveDebrisBaseClass, RemoveDebrisClass):
    def __init__(self, main, parent=None):
        super(RemoveDebris, self).__init__(parent)
        self.setupUi(self)
        self.main = main

        self.objectNbr.setMaximum(main.objectNbr.maximum())
        self.objectNbr.valueChanged.connect(self.showData)
        self.buttonBox.accepted.connect(self.remove)

    def showData(self):
        if self.objectNbr.value() == 0:
            self.num_m.display(0)
            self.num_d.display(0)
            self.num_Cm.display(0)
            self.num_etac.display(0)
        else:
            deb = self.main.debris_list[self.objectNbr.value()-1]
            self.num_m.display(deb._mass)
            self.num_d.display(deb._size)
            self.num_Cm.display(deb._Cm)
            self.num_etac.display(deb._etac)

    def remove(self):
        i = self.objectNbr.value()-1
        if i >= 0:
            ID = str(self.main.debris_list[i].ID)
            del self.main.debris_list[i]
            self.main.debrisConf.remove_section(ID)

