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
        self.laserConf = SCP(allow_no_value=True)

        # File Menu
        self.actionOpen_file.triggered.connect(self.open_file)
        self.actionClose.triggered.connect(self.close_application)
        # Edit Menu
        self.actionLoad_Lasers.triggered.connect(lambda: self.load_laser(
            self.get_filename('Laser Files (*.lcfg)')))
        # Run Menu

        # Laser Widget
        self.laserType.activated[str].connect(self.laser_choice)

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
        elif choice == "Custom":
            self.laserstack.setCurrentWidget(self.laserUndef)
        else:
            self.laserstack.setCurrentWidget(self.laserDef)
            self.laserDef.setDefaultLaserParam(dict(self.laserConf.items(str(choice))))

    def load_laser(self, filename):
        self.laserConf.read(str(filename))
        lasers = self.laserConf.sections()
        self.laserType.insertItems(self.laserType.count()-1, lasers)


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
