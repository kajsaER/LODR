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
        dl.update({'Repetition min':'0', 'Repetition max':'1e5','Pulse min':'1e-9',
            'Pulse max':'1e-3', 'Fire duration':'0', 'Fire min':'0', 'Fire max':'10'})
        self.laserConf = SCP(dl, allow_no_value=True)


        # File Menu
        self.actionOpen_file.triggered.connect(self.open_file)
        self.actionClose.triggered.connect(self.close_application)
        # Edit Menu
        self.actionLoad_Lasers.triggered.connect(lambda: self.load_laser(
            self.get_filename('Laser Files (*.lcfg)')))
        # Run Menu

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
        
        # Close Button
        self.closeBtn.clicked.connect(self.close_application)


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
                self.laser_type_list.append(laser)
                pos = pos+1


    def open_file(self):
        self.get_filename('LODR Files')


    def get_filename(self, pref):    
        filename = QtGui.QFileDialog.getOpenFileName(self.central_widget, 'Open File',
                self.filefolder, 'LODR Files (*.lodr);;Laser Files (*.lcfg);;All Files (*)', pref)
        self.filefolder = os.path.dirname(os.path.realpath(str(filename)))
        return filename

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
