from __future__ import division
from Subsystems import *

import sys
from PyQt4 import QtCore, QtGui, uic

qtCreatorMain = "Subsystems/GUI.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorMain)

class OperatorGUI(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(OperatorGUI, self).__init__(parent)
        self.setupUi(self)

        self.closeBtn.clicked.connect(self.close_application)
        self.actionClose.triggered.connect(self.close_application)
        self.laserType.activated[str].connect(self.laser_choice)

        self.laserwidget.setLayout(QtGui.QVBoxLayout())
        self.laserstack = QtGui.QStackedWidget()
        self.laserwidget.layout().addWidget(self.laserstack)
        self.laserEmpty = Laser_Widget()
        self.laserDef = DefinedLaser()
        self.laserUndef = UndefinedLaser()
        self.laserstack.addWidget(self.laserEmpty)
        self.laserstack.addWidget(self.laserDef)
        self.laserstack.addWidget(self.laserUndef)

    def laser_choice(self, choice):
        if choice == "Choose":
            self.laserstack.setCurrentWidget(self.laserEmpty)
        elif choice == "Custom":
            self.laserstack.setCurrentWidget(self.laserUndef)
        else:
            self.laserstack.setCurrentWidget(self.laserDef)
            self.laserDef.setDefaultLaserParam(choice)

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
