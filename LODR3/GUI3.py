import numpy as np
from Subsystems import *

from configparser import SafeConfigParser as SCP
import sys, os
import time, threading
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.patches import Circle as Circle
from matplotlib.figure import Figure
from PyQt4 import QtCore, QtGui, uic

#from random import random as rand

qtCreatorMain = "Subsystems/ui_Files/GUI.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorMain)

skipThis = 00
renameThis = 0o1
replaceThis = 0o2
skipAll = 10
renameAll = 11
replaceAll = 12

class OperatorGUI(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(OperatorGUI, self).__init__(parent)
        self.setupUi(self)
        self.di = 0
        self.filefolder = os.getcwd()
        self.formats = list() #QtCore.QStringList()
        for string in ['LODR Files (*.lodr)','Debris Files (*.dcfg)',
                       'Laser Files (*.lcfg)','Orbit Files (*.ocfg)',
                       'All Files (*)']:
            self.formats.append(string)
        
        self.openDiag = QtGui.QFileDialog(self.central_widget)
        self.openDiag.setAcceptMode(QtGui.QFileDialog.AcceptOpen)
        self.openDiag.setFileMode(QtGui.QFileDialog.ExistingFile)
        
        self.saveDiag = QtGui.QFileDialog(self.central_widget)
        self.saveDiag.setAcceptMode(QtGui.QFileDialog.AcceptSave)
        self.saveDiag.filterSelected.connect(self.updateSuffix)
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

        self.atmosphere = atmosphere()


        # File Menu
        self.actionOpen_file.triggered.connect(self.open_file)
        self.actionSave_file.triggered.connect(self.save_file)
        self.actionClose.triggered.connect(self.close_application)

        # Edit Menu
        self.actionLoad_Debris.triggered.connect(self.load_debris)
        self.actionAdd_Debris.triggered.connect(self.add_debris)
        self.actionRemove_Debris.triggered.connect(self.remove_debris)
        self.actionSave_Debris.triggered.connect(self.save_debris)
        
        self.actionLoad_Lasers.triggered.connect(self.load_laser)
        self.actionAdd_Laser.triggered.connect(self.add_laser)
        self.actionRemove_Laser.triggered.connect(self.remove_laser)
        self.actionSave_Laser.triggered.connect(self.save_laser)

        self.actionLoad_Orbits.triggered.connect(self.load_orbit)
        self.actionAdd_Orbits.triggered.connect(self.add_orbit)
        self.actionRemove_Orbits.triggered.connect(self.remove_orbit)
        self.actionSave_Orbits.triggered.connect(self.save_orbit)

        # Run Menu
        self.menuRun.menuAction().setVisible(False)
        self.running = False
        self.time_step = 240
        self.lock = threading.Lock()

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
        self.debris = None
        self.debris_list = []
        self.objectNbr.valueChanged.connect(self.change_debris)
        
        # Position

        # Orbit
        self.orbit_list = []
        
        # Buttons
        self.closeBtn.clicked.connect(self.close_application)
        self.closeBtn.setShortcut(QtGui.QKeySequence(QtGui.QKeySequence.Close))
        self.runBtn.clicked.connect(self.run_pushed)
        self.runBtn.setShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_R))

        # PlotView
        bgcolor =  np.asarray(self.palette().color(self.backgroundRole()).getRgb()[0:3])/255
        self.figure = Figure(tight_layout=True, facecolor=bgcolor)
#        self.figure.suptitle('Title', fontsize=15, y=0.995)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.plotLayout.addWidget(self.toolbar)
        self.plotLayout.addWidget(self.canvas)
        self.graph = self.figure.add_subplot(111)
        self.empty_plot()
        
################## End of main window init code #####################
     
    # Debris functions #
    def load_debris(self, filename=False, scp=False):
        if scp == False:
            if filename == False:
                filename = self.get_filename(formats=["Debris Files (*.dcfg)"])
            debrisConfTemp = SCP(allow_no_value=True)
            debrisConfTemp.optionxform = str
            debrisConfTemp.read(str(filename))
        else:
            debrisConfTemp = scp
        orbitdict = dict(debrisConfTemp.items("ORBITS"))
        orbitscp = self.dict2scp(orbitdict)
        self.load_orbit(scp=orbitscp)
        debrisConfTemp.remove_section("ORBITS")
        Debris = debrisConfTemp.sections()
        for deb in Debris:
            d = dict(debrisConfTemp.items(deb))
            orbname = d.get("orbit")
            o = set(orbitscp.items(orbname))
            O = set(self.orbitConf.items(orbname))
            if len(o & O) < 3:
                for orbname in self.orbitConf.sections():
                    O = set(self.orbitConf.items(orbname))
                    if len(o & O) == 3:
                        break
            o = dict(O)
            orb = orbit()
            orb.make(float(o.get("rp")), float(o.get("epsilon")), float(o.get("omega")))
            debname = (str(hex(int(float(d.get("mass")) + float(d.get("size")) + 
                        float(d.get("Cm"))*float(d.get("etac")) +
                        360/math.pi*float(d.get("nu"))))) + orbname)
            extra = 0
            n0 = debname
            while self.debrisConf.has_section(debname):
                debname = n0 + str(extra)
                extra += 1
            Deb = debris(str(debname), float(d.get("etac")), float(d.get("Cm")),
                         float(d.get("size")), float(d.get("mass")), orb, float(d.get("nu")))
            self.debrisConf.add_section(debname)
            for key in d:
                self.debrisConf.set(debname, key, d.get(key))
            self.debrisConf.set(debname, "orbit", orbname)
            self.debrisConf.set("ORBITS", orbname, str(self.orbitConf.items(orbname)))

            self.debris_list.append(Deb)
        self.objectNbr.setMaximum(len(self.debris_list))

    def add_debris(self):
        new_deb = NewDebris(self)
        new_deb.exec_()
        self.objectNbr.setMaximum(len(self.debris_list))

    def remove_debris(self):
        rem_deb = RemoveDebris(self)
        rem_deb.exec_()
        self.objectNbr.setMaximum(len(self.debris_list))

    def save_debris(self, filename):
        if filename == False:
            filename = self.set_filename('dcfg', formats=['Debris Files (*.dcfg)'])
        with open(filename, 'w') as writefile:
            self.debrisConf.write(writefile)

    def change_debris(self, i):
        if i == 0:
            self.num_m.display(0)
            self.num_d.display(0)
            self.num_Cm.display(0)
            self.num_etac.display(0)
            self.num_r.display(0)
            self.num_nu.display(0)
            self.num_v.display(0)
            self.num_rp.display(0)
            self.num_ra.display(0)
            self.num_omega.display(0)
            self.num_epsilon.display(0)
        else:
            self.debris = self.debris_list[i-1]
            self.num_m.display(self.debris._mass)
            self.num_d.display(self.debris._size)
            self.num_Cm.display(self.debris._Cm)
            self.num_etac.display(self.debris._etac)
            self.update_position()
            self.update_orbit()

    def debris_step(self):
        self.lock.acquire()
        self.di = 0
        self.plot_orbit()
        self.lock.release()
        while self.running:
            t1 = time.time()
            for i in range(self.time_step):
                self.lock.acquire()
                self.debris.step()
                self.lock.release()
            self.lock.acquire()
            self.plot_debris()
            self.update_position()
            td = time.time() - t1
#            print(td)
            ts = .1 - td
            self.lock.release()
            time.sleep(ts if ts > 0 else 0)

    def plot_debris(self):
#        print("Plot Debris")
        data = self.debris.plot_data()
        try:
            del self.graph.lines[self.graph.lines.index(self.deb_dot)]
        except (AttributeError, ValueError):
            pass
        self.deb_dot = self.graph.plot(data[0], data[1], 'ro')[0]
        self.canvas.draw()

    def update_position(self):
#        print("Update Position")
#        v = rand() # (self.debris._v)
        self.di += 1
#        self.num_r.display(int(self.debris._r/1000))
        self.num_r.display(self.di)
#        time.sleep(0.02)
        self.num_nu.display(self.di)
        self.num_v.display(self.di)
#        self.num_nu.display(int(math.degrees(self.debris._nu)))
#        print(self.debris._nu)
#        self.num_v.display(int(self.debris._v))

    def update_orbit(self):
#        print("Update orbit")
        orb = self.debris._orbit
        self.num_rp.display(orb.rp)
        self.num_ra.display(orb.ra)
        self.num_omega.display(orb.omega)
        self.num_epsilon.display(orb.ep)

    # Orbit functions #
    def load_orbit(self, filename=False, scp=False):
        if scp == False:
            if filename == False:
                filename = self.get_filename(formats=['Orbit Files (*.ocfg)'])
            orbitConfTemp = SCP(allow_no_value=True)
            orbitConfTemp.read(str(filename))
        else:
            orbitConfTemp = scp
        orbits = orbitConfTemp.sections()
        forAll = None
        for orb in orbits:
            if orb not in self.orbit_list:
                vals = dict(orbitConfTemp.items(orb))
                self.insert_orbit(orb, vals)
            elif len(set(orbitConfTemp.items(orb)) & set(self.orbitConf.items(orb))) == 3:
                pass
            else:
                if forAll == None:
                    action = DuplicateOrbit(orb).exec_()
                    if action >= 10:
                        action = action % 10
                        forAll = action
                else:
                    action = forAll
                if action == 0: # Skip
                    pass
                elif action == 1: # Rename
                    name = orb
                    while name in self.orbit_list:
                        name = str(QtGui.QInputDialog.getText(self.central_widget,
                                "Rename Orbit", "Name")[0])
                    vals = dict(orbitConfTemp.items(orb))
                    self.insert_orbit(name, vals)
                elif action == 2: # Replace
                    vals = dict(orbitConfTemp.items(orb))
                    self.insert_orbit(orb, vals)
        self.orbit_list.sort()

    def insert_orbit(self, name, vals):
        if not self.orbitConf.has_section(name):
            self.orbitConf.add_section(name)
        self.orbitConf.set(name, "rp", vals.get("rp"))
        self.orbitConf.set(name, "epsilon", vals.get("epsilon"))
        self.orbitConf.set(name, "omega", vals.get("omega"))
        self.orbit_list.append(name)

    def add_orbit(self):
        self.new_orb = NewOrbit(self)
        self.new_orb.exec_()

    def remove_orbit(self):
        rem_orb = RemoveOrbit(self)
        rem_orb.exec_()

    def save_orbit(self, filename):
        if filename == False:
            filename = self.set_filename('ocfg', formats=['Orbit Files (*.ocfg)'])
        with open(filename, 'w') as writefile:
            self.orbitConf.write(writefile)

    def plot_approx_orbit(self):
        data = self.debris._orbit.plot_approx_data()
        self.graph.plot(data[0], data[1], ':')
        self.graph.axis('equal')
        self.canvas.draw()

    def plot_orbit(self):
        data = self.debris._orbit.plot_data()
        self.graph.plot(data[0], data[1])
        self.graph.axis('equal')
        self.canvas.draw()


    # Laser functions #
    def load_laser(self, filename=False, scp=False):
        if scp == False:
            if filename == False:
                filename = self.get_filename(formats=['Laser Files (*.lcfg)'])
            laserConfTemp = SCP(allow_no_value=True)
            laserConfTemp.read(str(filename))
        else:
            laserConfTemp = scp
        lasers = laserConfTemp.sections()
        forAll = None
        for laser in lasers:
            if laser not in self.laserConf.sections():
                vals = dict(laserConfTemp.items(laser))
                self.insert_laser(laser, vals)
            elif len(set(laserConfTemp.items(laser)) & set(self.laserConf.items(laser))) == 7:
                pass
            else:
                if forAll == None:
                    action = DuplicateLaser(laser).exec_()
                    if action >= 10:
                        action = action % 10
                        forAll = action
                else:
                    action = forAll
                if action == 0: # Skip
                    pass
                elif action == 1: # Rename
                    name = laser
                    while name in self.laserConf.sections():
                        name = str(QtGui.QInputDialog.getText(self.central_widget,
                                "Rename Laser", "Name")[0])
                    vals = dict(laserConfTemp.items(laser))
                    self.insert_laser(name, vals)
                elif action == 2: # Replace
                    vals = dict(laserConfTemp.items(laser))
                    self.insert_laser(laser, vals)

    def insert_laser(self, name, vals):
        if 'Custom' in self.laser_type_list:
            pos = self.laserType.count()-1
        else:
            pos = self.laserType.count()
        if not self.laserConf.has_section(name):
            self.laserConf.add_section(name)
        for key in vals:
            self.laserConf.set(name, key, vals.get(key))
        self.laserType.insertItem(pos, name)
        self.laser_type_list.insert(pos, name)

    def add_laser(self):
        new_laser = NewLaser(self)
        new_laser.exec_()

    def remove_laser(self):
        rem_laser = RemoveLaser(self)
        rem_laser.exec_()

    def save_laser(self, filename):
        if filename == False:
            filename = self.set_filename('lcfg', formats=['Laser Files (*.lcfg)'])
        with open(filename, 'w') as writefile:
            self.laserConf.write(writefile)

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

    def fire(self):
        self.lasersystem.fire(self.antenna, self.debris,
                float(self.laserstack.currentWidget().get_duration()),
                self.atmosphere)

    # Other functions #
    def open_file(self):
        filename = str(self.get_filename(pref='LODR Files (*.lodr)'))
        if filename != 'None':
            if filename.endswith('lodr'):
                confTemp = SCP(allow_no_value=True)
                confTemp.optionxform = str
                confTemp.read(str(filename))
                for section in confTemp.sections():
                    dictionary = dict(confTemp.items(section))
                    scp = self.dict2scp(dictionary)
                    exec("self.load_" + str(section).lower() + "(scp=scp)")
            elif filename.endswith('dcfg'): # Debris files
                self.load_debris(filename=filename)
            elif filename.endswith('lcfg'): # Laser files
                self.load_laser(filename=filename)
            elif filename.endswith('ocfg'): # Orbit files
                self.load_orbit(filename=filename)
            else:
                QtGui.QMessageBox.warning(self.central_widget, 'Unsupported format',
                        'The file you chose has an unsupported format. \n' +
                        'Please choose a different file', buttons=QtGui.QMessageBox.Ok,
                        defaultButton=QtGui.QMessageBox.NoButton)
    
    def save_file(self):
        filename = str(self.set_filename('lodr', pref='LODR Files (*.lodr)'))
        if filename != 'None':
            if filename.endswith('lodr'):
                confTemp = SCP(allow_no_value=True)
                confTemp.optionxform = str
                confTemp.add_section("LASER")
                for name in self.laserConf.sections():
                    if name != "Custom":
                        confTemp.set("LASER", name, str(self.laserConf.items(name)))
                confTemp.add_section("ORBIT")
                for name in self.orbitConf.sections():
                    confTemp.set("ORBIT", name, str(self.orbitConf.items(name)))
                confTemp.add_section("DEBRIS")
                for name in self.debrisConf.sections():
                    confTemp.set("DEBRIS", name, str(self.debrisConf.items(name)))
                with open(filename, 'w') as writefile:
                    confTemp.write(writefile)
            elif filename.endswith('dcfg'): # Debris files
                self.save_debris(filename=filename)
            elif filename.endswith('lcfg'): # Laser files
                self.save_laser(filename=filename)
            elif filename.endswith('ocfg'): # Orbit files
                self.save_orbit(filename=filename)
            else:
                QtGui.QMessageBox.warning(self.central_widget, 'Unsupported format',
                        'The file you chose has an unsupported format. \n' +
                        'Please choose a different file', buttons=QtGui.QMessageBox.Ok,
                        defaultButton=QtGui.QMessageBox.NoButton)
    
    def get_filename(self, pref=None, formats=None):
        if formats == None:
            formats = self.formats
        if pref == None:
            pref = formats[0]
        self.openDiag.setNameFilters(formats)
        self.openDiag.setDirectory(self.filefolder)
        self.openDiag.selectNameFilter(pref)
        if (self.openDiag.exec_()):
            filename = self.openDiag.selectedFiles()[0]
            self.filefolder = os.path.dirname(os.path.realpath(str(filename)))
            return filename

    def set_filename(self, suffix, pref=None, formats=None):
        if formats == None:
            formats = self.formats
        if pref == None:
            pref = formats[0]
        self.saveDiag.setNameFilters(formats)
        self.saveDiag.selectNameFilter(pref)
        self.saveDiag.setDefaultSuffix(suffix)
        if (self.saveDiag.exec_()):
            filename = self.saveDiag.selectedFiles()[0]
            self.filefolder = os.path.dirname(os.path.realpath(str(filename)))
            return filename

    def updateSuffix(self, nameFilter):
        namefilter = str(nameFilter)
        if namefilter.rfind('*.') > -1:
            part = namefilter.rpartition('*.')[2]
            suffix = part[0:len(part)-1]
        else:
            suffix = 'txt'
        self.saveDiag.setDefaultSuffix(suffix)

    def empty_plot(self):
        self.graph.clear()
        self.graph.add_patch(Circle((0, 0), consts.Re+160e+03, color='b', alpha=0.2))
        self.graph.add_patch(Circle((0, 0), consts.Re, color='g', alpha=0.5))
        self.graph.margins(0.1, tight=False)
        self.graph.axis('equal')
        self.canvas.draw()

    def dict2scp(self, dictionary):
        scp = SCP(allow_no_value=True)
        scp.optionxform = str
        for sec in list(dictionary.keys()):
            scp.add_section(sec)
            vals = dict(eval(dictionary.get(sec)))
            for key in vals:
                scp.set(sec, key, str(vals.get(key)))
        return scp

    def run_app(self):
        i = 0
        self.plot_orbit()
        while self.running:
            print(i)
            i += 1
            self.debris_step()
            self.plot_debris()
            time.sleep(1)

    def run_pushed(self):
        if self.debris != None:
            self.running = not self.running
            if self.running:
                self.debris_thread = threading.Thread(target=self.debris_step).start()
        else:
            QtGui.QMessageBox.information(self.central_widget, "Error",
                                          "No debris chosen", QtGui.QMessageBox.Ok)
            self.running = False
        print("Run function needs to be implemented")

    def close_application(self):
        choice = QtGui.QMessageBox.question(self.central_widget, "Close",
                                            "Are you sure you want to close the application?",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            sys.exit()
        else:
            pass



if __name__ == "__main__":

    sys.settrace
    app = QtGui.QApplication(sys.argv)
    window = OperatorGUI()
    window.show()
    sys.exit(app.exec_())
