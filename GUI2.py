from __future__ import division
from Subsystems import *

from ConfigParser import SafeConfigParser as SCP
import sys, os
from PyQt4 import QtCore, QtGui, uic

qtCreatorMain = "Subsystems/GUI.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorMain)

class OperatorGUI(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(OperatorGUI, self).__init__(parent)
        self.setupUi(self)
        self.filefolder = os.getcwd()
        dl = dict.fromkeys(['Power', 'Energy', 'Lambda', 'M2', 'Cb',
                            'Repetition rate', 'Pulse duration'])
        dl.update({'Repetition rate min':'1E+00', 'Repetition rate max':'1E+05',
            'Pulse duration min':'1E-09', 'Pulse duration max':'1E-03',
            'Fire duration':'1E+00', 'Fire duration min':'1E-06', 'Fire duration max':'1E+01'})
        self.laserConf = SCP(dl, allow_no_value=True)
        
        self.debrisConf = SCP(allow_no_value=False)
        self.debrisConf.add_section("ORBITS")
        self.debrisConf.optionxform = str
        self.orbitConf = SCP(allow_no_value=True)


        # File Menu
        self.actionOpen_file.triggered.connect(self.open_file)
        self.actionSave_file.triggered.connect(self.save_file)
        self.actionClose.triggered.connect(self.close_application)

        # Edit Menu
        self.actionLoad_Debris.triggered.connect(lambda: self.load_debris(
            self.get_filename('Debris Files (*.dcfg)')))
        self.actionAdd_Debris.triggered.connect(self.add_debris)
        self.actionRemove_Debris.triggered.connect(self.remove_debris)
        self.actionSave_Debris.triggered.connect(self.save_debris)
        
        self.actionLoad_Lasers.triggered.connect(lambda: self.load_laser(
            self.get_filename('Laser Files (*.lcfg)')))
        self.actionAdd_Laser.triggered.connect(self.add_laser)
        self.actionRemove_Laser.triggered.connect(self.remove_laser)
        self.actionSave_Laser.triggered.connect(self.save_laser)

        self.actionLoad_Orbits.triggered.connect(lambda: self.load_orbits(
            self.get_filename('Orbit Files (*.ocfg)')))
        self.actionAdd_Orbits.triggered.connect(self.add_orbit)
        self.actionRemove_Orbits.triggered.connect(self.remove_orbit)
        self.actionSave_Orbits.triggered.connect(self.save_orbit)

        # Run Menu
        self.menuRun.menuAction().setVisible(False)

        # Laser Widget
        self.laserType.activated[str].connect(self.laser_choice) 
        self.laser_type_list = ['Choose']
        
        self.lasersystem = laser()
        self.laserwidget.setLayout(QtGui.QVBoxLayout())
        self.laserstack = QtGui.QStackedWidget()
        self.laserwidget.layout().addWidget(self.laserstack)
        self.laserEmpty = Laser_Widget(self)
        self.laserDef = DefinedLaser(self)
        self.laserUndef = UndefinedLaser(self)
        self.laserstack.addWidget(self.laserEmpty)
        self.laserstack.addWidget(self.laserDef)
        self.laserstack.addWidget(self.laserUndef)

        # Antenna
        self.antenna = antenna(0,0)
        self.antennaD.setValidator(QtGui.QDoubleValidator())
        self.antennaD.editingFinished.connect(lambda: self.antenna.set_D(self.antennaD.text()))
        self.antennaEff.valueChanged.connect(lambda value: self.antenna.set_ratio(
            float(self.antennaEff.value()/100)))

        # Debris
        self.debris_list = []
        self.objectNbr.valueChanged.connect(self.change_debris)
        
        # Position

        # Orbit
        self.orbit_list = []
        
        # Buttons
        self.closeBtn.clicked.connect(self.close_application)
        self.runBtn.clicked.connect(self.run_app)
     
    # Debris functions #
    def load_debris(self, filename):
        self.debrisConf.read(str(filename))
        Debris = self.debrisConf.sections()
        orbits = dict(self.debrisConf.items("ORBITS"))
        for orb in orbits.keys():
            if orb not in self.orbitConf.sections():
                self.orbitConf.add_section(orb)
            exec('vals = dict('+orbits.get(orb)+')')
            self.orbitConf.set(orb, "a", vals.get("a"))
            self.orbitConf.set(orb, "epsilon", vals.get("epsilon"))
            self.orbitConf.set(orb, "omega", vals.get("omega"))
            self.orbit_list.append(str(orb))
        self.orbit_list.sort()
        for deb in Debris:
            if deb != "ORBITS":
                d = dict(self.debrisConf.items(deb))
                orb = orbit()
                o = dict(self.orbitConf.items(d.get("orbit")))
                orb.make(float(o.get("a")), float(o.get("epsilon")), float(o.get("omega")))
                Deb = debris(float(d.get("etac")), float(d.get("Cm")), float(d.get("size")),
                             float(d.get("mass")), orb, float(d.get("nu")))
                self.debris_list.append(Deb)
        self.objectNbr.setMaximum(len(self.debris_list))

    def add_debris(self):
        new_deb = NewDebris(self)
        new_deb.exec_()
        self.objectNbr.setMaximum(len(self.debris_list))

    def remove_debris(self):
        rem_deb = RemoveDebris(self)
        rem_deb.exec_()

    def save_debris(self):
        print "Save debris needs to be implemented"

    def change_debris(self, i):
        print "Switching debris needs to be implemented"
        print i

    # Orbit functions #
    def load_orbits(self, filename):
        self.orbitConf.read(str(filename))
        orbits = self.orbitConf.sections()
        for orb in orbits:
            if orb not in self.orbit_list:
                self.orbit_list.append(orb)
        self.orbit_list.sort()

    def add_orbit(self):
        self.new_orb = NewOrbit(self)
        self.new_orb.exec_()

    def remove_orbit(self):
        rem_orb = RemoveOrbit(self)
        rem_orb.exec_()

    def save_orbit(self):
        print "Save orbit needs to be implemented"

    # Laser functions #
    def load_laser(self, filename):
        self.laserConf.read(str(filename))
        lasers = self.laserConf.sections()
        if 'Custom' in self.laser_type_list:
            pos = self.laserType.count()-1
        else:
            pos = self.laserType.count()
        for laser in lasers:
            if laser not in self.laser_type_list:
                self.laserType.insertItem(pos, laser)
                self.laser_type_list.insert(pos, laser)
                pos = pos+1

    def add_laser(self):
        new_laser = NewLaser(self)
        new_laser.exec_()

    def remove_laser(self):
        print "Remove laser needs to be implemented"

    def save_laser(self):
        print "Save laser needs to be implemented"

    def laser_choice(self, choice):
        if choice == "Choose":
            self.laserstack.setCurrentWidget(self.laserEmpty)
            LT = self.laserConf.defaults()
            self.lasersystem.switch(LT)
        elif choice == "Custom":
            self.laserstack.setCurrentWidget(self.laserUndef)
            LT = dict(self.laserConf.items(str(choice)))
            self.laserUndef.setDefaultLaserParam(LT)
            self.lasersystem.switch(LT)
        else:
            self.laserstack.setCurrentWidget(self.laserDef)
            LT = dict(self.laserConf.items(str(choice)))
            self.laserDef.setDefaultLaserParam(LT)
            self.lasersystem.switch(LT)

    # Other functions #
    def open_file(self):
        self.get_filename('LODR Files')

    def save_file(self):
        print "Save file needs to be implemented"

    def get_filename(self, pref):    
        filename = QtGui.QFileDialog.getOpenFileName(self.central_widget, 'Open File',
                self.filefolder, ('LODR Files (*.lodr);;Debris Files (*.dcfg);;'+
                                  'Laser Files (*.lcfg);;Orbit Files (*.ocfg);;'+
                                  'All Files (*)'), pref)
        self.filefolder = os.path.dirname(os.path.realpath(str(filename)))
        return filename

    def run_app(self):
        print "Run function needs to be implemented"

    def close_application(self):
        choice = QtGui.QMessageBox.question(self.central_widget, "Close",
                                            "Are you sure you want to close the application?",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            sys.exit()
        else:
            pass



if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    window = OperatorGUI()
    window.show()
    sys.exit(app.exec_())
