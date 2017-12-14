from PyQt4 import QtCore, QtGui, uic

qtCreatorNewDebris = "Subsystems/NewDebris.ui"
NewDebrisClass, NewDebrisBaseClass = uic.loadUiType(qtCreatorNewDebris)


class NewDebris(NewDebrisBaseClass, NewDebrisClass):
    def __init__(self, main, parent=None):
        super(NewDebris, self).__init__(parent)
        self.setupUi(self)
        self.main = main
