from PyQt5 import QtCore, QtWidgets, QtGui, uic
import math
from Subsystems.orbit import orbit
from Subsystems.debris import debris

qtCreatorNewDebris = "Subsystems/ui_Files/NewDebris.ui"
NewDebrisClass, NewDebrisBaseClass = uic.loadUiType(qtCreatorNewDebris)

qtCreatorRemoveDebris = "Subsystems/ui_Files/RemoveDebris.ui"
RemoveDebrisClass, RemoveDebrisBaseClass = uic.loadUiType(qtCreatorRemoveDebris)

mmin = 0        # Minimum mass
mmax = 100      # Maximum mass
dmin = 0        # Minimum diameter
dmax = 5        # Maximun diameter
Cmmin = 0       # Minimum momentum coupling coefficient
Cmmax = 400     # Maximum momentum coupling coefficient
etacmin = 0     # Minimum combined efficiency factor
etacmax = 1     # Maximum combined efficiency factor
numin = 0       # Minimum true anomaly
numax = 2*math.pi   # Maximum true anomaly

class NewDebris(NewDebrisBaseClass, NewDebrisClass):
    def __init__(self, main, parent=None):
        super(NewDebris, self).__init__(parent)
        self.setupUi(self)
        self.main = main
        self.orbitList = []     # List of all available orbits
        for orbit in self.main.orbit_list:  # Add lists from main
            self.orbitList.append(orbit)
            self.orbitListWidget.addItem(orbit)
        
        self.validm = False
        self.validd = False
        self.validCm = False
        self.validetac = False
        self.validnu = False
        
        # Require double() values
        self.m.setValidator(QtGui.QDoubleValidator())
        self.d.setValidator(QtGui.QDoubleValidator())
        self.Cm.setValidator(QtGui.QDoubleValidator())
        self.etac.setValidator(QtGui.QDoubleValidator())
        self.nu.setValidator(QtGui.QDoubleValidator())
        
        # Run check when a variable is edited
        self.m.editingFinished.connect(self.updatem)
        self.d.editingFinished.connect(self.updated)
        self.Cm.editingFinished.connect(self.updateCm)
        self.etac.editingFinished.connect(self.updateetac)
        self.nu.editingFinished.connect(self.updatenu)
        self.orbitListWidget.currentRowChanged.connect(self.checkOK)
        
        # Make buttons and disable OK button 
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
        self.buttonBox.accepted.connect(self.OKClicked)
        self.newOrbitButton.clicked.connect(self.add_orbit)

    def updatem(self):  # Check if mass is in the valid range
        m = float(self.m.text())
        if m > mmin and m <= mmax:
            self.valuem = m
            self.validm = True
        else:
            self.m.setText("invaild")
            self.validm = False
        self.checkOK()  # Check if OK should be enabled
    
    def updated(self):  # Check if diameter is in the valid range
        d = float(self.d.text())
        if d > dmin and d <= dmax:
            self.valued = d
            self.validd = True
        else:
            self.d.setText("invaild")
            self.validd = False
        self.checkOK()  # Check if OK should be enabled

    def updateCm(self): # Check if Cm is in the valid range
        Cm = float(self.Cm.text())
        if Cm > Cmmin and Cm <= Cmmax:
            self.valueCm = Cm
            self.validCm = True
        else:
            self.Cm.setText("invaild")
            self.validCm = False
        self.checkOK()  # Check if OK should be enabled

    def updateetac(self):   # Check if ηc is in the valid range
        etac = float(self.etac.text())
        if etac > etacmin and etac <= etacmax:
            self.valueetac = etac
            self.validetac = True
        else:
            self.etac.setText("invaild")
            self.validetac = False
        self.checkOK()  # Check if OK should be enabled

    def updatenu(self): # Check if ν is in the valid range
        nu = float(self.nu.text())
        if nu > numin and nu <= numax:
            self.valuenu = nu
            self.validnu = True
        else:
            self.nu.setText("invaild")
            self.validnu = False
        self.checkOK()  # Check if OK should be enabled

    def checkOK(self):  # Check if OK to save new debris
        if (self.orbitListWidget.currentRow() > -1 and self.validm and 
                self.validd and self.validCm and
                self.validetac and self.validnu):   # If all variabled are valid
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
    
    def add_orbit(self):    # Add a new orbit
        self.main.add_orbit()   # Run add_orbit from main window
        for orbit in self.main.orbit_list:  # Add all orbits to local list
            if orbit not in self.orbitList:
                self.orbitList.append(orbit)
                self.orbitListWidget.addItem(orbit)
                self.orbitListWidget.sortItems(order=QtCore.Qt.AscendingOrder)

    def OKClicked(self):    # When OK button is clicked
        orbname = str(self.orbitListWidget.currentItem().text())
        name = (str(hex(int(self.valuem + self.valued + # Determin ID for debris 
                self.valueCm*self.valueetac + 360/math.pi*self.valuenu))) + orbname)
        extra = 0
        n0 = name
        while self.main.debrisConf.has_section(name): # If ID already exists
            name = n0 + str(extra)      # Add an int to the end
            extra += 1                  # Increase the int until unique
        orbvals = self.main.orbitConf.items(orbname)    # Get orbit from main list
        self.main.debrisConf.add_section(name)      # Add section in main Conf
        self.main.debrisConf.set(name, "mass", str(self.valuem))
        self.main.debrisConf.set(name, "size", str(self.valued))
        self.main.debrisConf.set(name, "Cm", str(self.valueCm))
        self.main.debrisConf.set(name, "etac", str(self.valueetac))
        self.main.debrisConf.set(name, "nu", str(self.valuenu))
        self.main.debrisConf.set(name, "orbit", orbname)
        self.main.debrisConf.set("ORBITS", orbname, str(orbvals))

        orb = orbit()       # Make new orbit with the values
        o = dict(orbvals)
        orb.make(float(o.get("rp")), float(o.get("epsilon")), float(o.get("omega")))
        deb = debris(name, self.valueetac, self.valueCm,    # Make debris
                     self.valued, self.valuem, orb, self.valuenu)
        self.main.debris_list.append(deb)   # Add debris to main list



class RemoveDebris(RemoveDebrisBaseClass, RemoveDebrisClass):
    def __init__(self, main, parent=None):
        super(RemoveDebris, self).__init__(parent)
        self.setupUi(self)
        self.main = main

        # Setup inputs
        self.objectNbr.setMaximum(main.objectNbr.maximum())
        self.objectNbr.valueChanged.connect(self.showData)
        self.buttonBox.accepted.connect(self.remove)

    def showData(self):     # Update shown data when chosen
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

    def remove(self):   # Remove chosen debris from main list and Conf
        i = self.objectNbr.value()-1
        if i >= 0:
            ID = str(self.main.debris_list[i].ID)
            del self.main.debris_list[i]
            self.main.debrisConf.remove_section(ID)
