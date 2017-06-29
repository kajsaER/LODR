#!/usr/bin/python

import sys
from PyQt4 import QtGui, QtCore


class GUI(QtGui.QMainWindow):

    def __init__(self):
        super(GUI, self).__init__()
        self.setGeometry(50,50,500,300)
        self.setWindowTitle("LODR")
        #self.setWindowIcon(QtGui.QIcon('path'))
        
        ######## Main menu bar buttons #########
        # Quit button #
        quitAction = QtGui.QAction("&Quit", self)
        quitAction.setShortcut("Ctrl+Q")
        quitAction.setStatusTip('Close program')
        quitAction.triggered.connect(self.close_application)

        ######## Status bar ########
        self.statusBar()

        ######## Main menu bar ########
        mainMenu = self.menuBar()
        
        fileMenu = mainMenu.addMenu("&File")
        fileMenu.addAction(quitAction)

        editMenu = mainMenu.addMenu("&Edit")

        runMenu = mainMenu.addMenu("&Run")

        windowMenu = mainMenu.addMenu("&Window")

        helpMenu = mainMenu.addMenu("&Help")
        
        ######## Set style ########
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("Plastique"))
        ## Go to home window
        self.home()

    ######## Windows ########
    def home(self):
        btn = QtGui.QPushButton("Quit", self)
        btn.clicked.connect(self.close_application)
        btn.resize(btn.sizeHint())#100,100)
        btn.move(0,100) 	#the coordinates for the top left corner of the button

        #### Tool bar ####
#        extractAction = QtGui.QAction(QtGui.QIcon('path'), 'Hover text', self)
#        extractAction.triggered.connect(self.what_to_do)
#        self.toolBar = self.addToolBar("Tool Bar")
#        self.toolBar.addAction(extractAction)

        #### Check boxes ####
        checkBox = QtGui.QCheckBox('Show plot', self)
        checkBox.move(0, 25)
        checkBox.stateChanged.connect(self.show_plot)

        #### Progress bar ####
        self.progress = QtGui.QProgressBar(self)
        self.progress.setGeometry(200, 80, 250, 20)

        self.dwlbtn = QtGui.QPushButton("Download", self)
        self.dwlbtn.move(200, 120)
        self.dwlbtn.clicked.connect(self.download)
        
        print(self.style().objectName())

        self.show()

    ######## Applications ########
    def close_application(self):
        choise = QtGui.QMessageBox.question(self, 'Quit', "Are you sure you want to quit?", 
                                            QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
        if choise == QtGui.QMessageBox.Yes :
            sys.exit()
        else:
            pass

    def show_plot(self, state):
        if state == QtCore.Qt.Checked:
            # Code for showing the plot
            print "Showing plot"
        else:
            # Code for hiding the plot
            print "Hiding plot"

    def download(self):
        self.completed = 0

        while self.completed < 100:
            self.completed += 1e-5
            self.progress.setValue(self.completed)

def run():
    app = QtGui.QApplication(sys.argv)
    Gui = GUI()
    sys.exit(app.exec_())


run()

