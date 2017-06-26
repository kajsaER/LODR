#!/usr/bin/python

import sys
from PyQt4 import QtGui, QtCore

#app = QtGui.QApplication(sys.argv)
#window = QtGui.QWidget()

#window.setGeometry(0,0,500,300)
#window.setWindowTitle("LODR")

#window.show()

#sys.exit(app.exec_())

class GUI(QtGui.QMainWindow):

    def __init__(self):
        super(GUI, self).__init__()
        self.setGeometry(50,50,500,300)
        self.setWindowTitle("LODR")
        #self.setWindowIcon(QtGui.QIcon('path'))
        self.home()

    def home(self):
        btn = QtGui.QPushButton("Quit", self)
        btn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        btn.resize(btn.sizeHint())#100,100)
        btn.move(100,100)
        self.show()

app = QtGui.QApplication(sys.argv)
Gui = GUI()
sys.exit(app.exec_())

