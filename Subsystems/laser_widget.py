from PyQt4 import QtCore, QtGui, uic

qtCreatorLaser = "Subsystems/laser_widget.ui"
laser_widget, laserBaseClass = uic.loadUiType(qtCreatorLaser)
qtCreatorDefinedLaser = "Subsystems/definedLaser.ui"
DefinedLaserWidget, DefinedLaserBaseClass = uic.loadUiType(qtCreatorDefinedLaser)
qtCreatorUndefinedLaser = "Subsystems/undefinedLaser.ui"
UndefinedLaserWidget, UndefinedLaserBaseClass = uic.loadUiType(qtCreatorUndefinedLaser)

class Laser_Widget(laserBaseClass, laser_widget):
    def __init__(self, parent=None):
        super(Laser_Widget, self).__init__(parent)
        self.setupUi(self)


class DefinedLaser(DefinedLaserBaseClass, DefinedLaserWidget):
    def __init__(self, parent=None):
        super(DefinedLaser, self).__init__(parent)
        self.setupUi(self)

    def setDefaultLaserParam(self, LaserType):
        self.freqDub.setChecked(False)
        # self.num_P
        # self.num_W
        # self.num_lambda
        # self.num_M2
        # self.num_Cb
        # self.num_frep
        # self.slide_frep
        # self.num_tau
        # self.slide_tau
        # self.num_T
        # self.slide_T

class UndefinedLaser(UndefinedLaserBaseClass, UndefinedLaserWidget):
    def __init__(self, parent=None):
        super(UndefinedLaser, self).__init__(parent)
        self.setupUi(self)

