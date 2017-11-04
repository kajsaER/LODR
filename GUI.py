# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Subsystems/GUI.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(812, 569)
        MainWindow.setMinimumSize(QtCore.QSize(0, 0))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.laserType = QtGui.QComboBox(self.centralwidget)
        self.laserType.setMaximumSize(QtCore.QSize(100, 16777215))
        self.laserType.setObjectName(_fromUtf8("laserType"))
        self.laserType.addItem(_fromUtf8(""))
        self.laserType.addItem(_fromUtf8(""))
        self.laserType.addItem(_fromUtf8(""))
        self.laserType.addItem(_fromUtf8(""))
        self.laserType.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.laserType, 1, 1, 1, 1)
        self.label_laser = QtGui.QLabel(self.centralwidget)
        self.label_laser.setMinimumSize(QtCore.QSize(35, 0))
        self.label_laser.setMaximumSize(QtCore.QSize(35, 16777215))
        self.label_laser.setObjectName(_fromUtf8("label_laser"))
        self.gridLayout.addWidget(self.label_laser, 1, 0, 1, 1)
        self.closeBtn = QtGui.QPushButton(self.centralwidget)
        self.closeBtn.setMinimumSize(QtCore.QSize(80, 25))
        self.closeBtn.setMaximumSize(QtCore.QSize(80, 25))
        self.closeBtn.setObjectName(_fromUtf8("closeBtn"))
        self.gridLayout.addWidget(self.closeBtn, 8, 0, 1, 3)
        spacerItem = QtGui.QSpacerItem(20, 36, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 7, 0, 1, 1)
        self.plotView = QtGui.QGraphicsView(self.centralwidget)
        self.plotView.setEnabled(True)
        self.plotView.setObjectName(_fromUtf8("plotView"))
        self.gridLayout.addWidget(self.plotView, 0, 5, 9, 1)
        self.laserwidget = QtGui.QWidget(self.centralwidget)
        self.laserwidget.setMinimumSize(QtCore.QSize(124, 210))
        self.laserwidget.setObjectName(_fromUtf8("laserwidget"))
        self.gridLayout.addWidget(self.laserwidget, 2, 0, 1, 5)
        self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_2.setMinimumSize(QtCore.QSize(312, 122))
        self.groupBox_2.setTitle(_fromUtf8(""))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.DebrisGroup = QtGui.QGroupBox(self.groupBox_2)
        self.DebrisGroup.setGeometry(QtCore.QRect(0, 0, 101, 111))
        self.DebrisGroup.setObjectName(_fromUtf8("DebrisGroup"))
        self.num_etac = QtGui.QLCDNumber(self.DebrisGroup)
        self.num_etac.setGeometry(QtCore.QRect(41, 80, 51, 23))
        self.num_etac.setObjectName(_fromUtf8("num_etac"))
        self.label_etac = QtGui.QLabel(self.DebrisGroup)
        self.label_etac.setGeometry(QtCore.QRect(10, 80, 30, 20))
        self.label_etac.setObjectName(_fromUtf8("label_etac"))
        self.label_Cm = QtGui.QLabel(self.DebrisGroup)
        self.label_Cm.setGeometry(QtCore.QRect(-1, 60, 41, 20))
        self.label_Cm.setObjectName(_fromUtf8("label_Cm"))
        self.label_m = QtGui.QLabel(self.DebrisGroup)
        self.label_m.setGeometry(QtCore.QRect(10, 20, 30, 20))
        self.label_m.setObjectName(_fromUtf8("label_m"))
        self.num_d = QtGui.QLCDNumber(self.DebrisGroup)
        self.num_d.setGeometry(QtCore.QRect(41, 40, 51, 23))
        self.num_d.setObjectName(_fromUtf8("num_d"))
        self.num_m = QtGui.QLCDNumber(self.DebrisGroup)
        self.num_m.setGeometry(QtCore.QRect(41, 20, 51, 23))
        self.num_m.setObjectName(_fromUtf8("num_m"))
        self.label_d = QtGui.QLabel(self.DebrisGroup)
        self.label_d.setGeometry(QtCore.QRect(10, 40, 30, 20))
        self.label_d.setObjectName(_fromUtf8("label_d"))
        self.num_Cm = QtGui.QLCDNumber(self.DebrisGroup)
        self.num_Cm.setGeometry(QtCore.QRect(41, 60, 51, 23))
        self.num_Cm.setObjectName(_fromUtf8("num_Cm"))
        self.PositionGroup = QtGui.QGroupBox(self.groupBox_2)
        self.PositionGroup.setGeometry(QtCore.QRect(110, 0, 91, 101))
        self.PositionGroup.setObjectName(_fromUtf8("PositionGroup"))
        self.num_v = QtGui.QLCDNumber(self.PositionGroup)
        self.num_v.setGeometry(QtCore.QRect(40, 60, 50, 23))
        self.num_v.setObjectName(_fromUtf8("num_v"))
        self.label_r = QtGui.QLabel(self.PositionGroup)
        self.label_r.setGeometry(QtCore.QRect(20, 20, 20, 20))
        self.label_r.setObjectName(_fromUtf8("label_r"))
        self.label_v = QtGui.QLabel(self.PositionGroup)
        self.label_v.setGeometry(QtCore.QRect(20, 60, 20, 20))
        self.label_v.setObjectName(_fromUtf8("label_v"))
        self.label_nu = QtGui.QLabel(self.PositionGroup)
        self.label_nu.setGeometry(QtCore.QRect(20, 40, 20, 20))
        self.label_nu.setObjectName(_fromUtf8("label_nu"))
        self.num_nu = QtGui.QLCDNumber(self.PositionGroup)
        self.num_nu.setGeometry(QtCore.QRect(40, 40, 50, 23))
        self.num_nu.setObjectName(_fromUtf8("num_nu"))
        self.num_r = QtGui.QLCDNumber(self.PositionGroup)
        self.num_r.setGeometry(QtCore.QRect(40, 20, 50, 23))
        self.num_r.setObjectName(_fromUtf8("num_r"))
        self.OrbitGroup = QtGui.QGroupBox(self.groupBox_2)
        self.OrbitGroup.setGeometry(QtCore.QRect(220, 0, 98, 111))
        self.OrbitGroup.setObjectName(_fromUtf8("OrbitGroup"))
        self.num_epsilon = QtGui.QLCDNumber(self.OrbitGroup)
        self.num_epsilon.setGeometry(QtCore.QRect(40, 80, 51, 23))
        self.num_epsilon.setObjectName(_fromUtf8("num_epsilon"))
        self.label_epsilon = QtGui.QLabel(self.OrbitGroup)
        self.label_epsilon.setGeometry(QtCore.QRect(20, 80, 20, 20))
        self.label_epsilon.setObjectName(_fromUtf8("label_epsilon"))
        self.num_rp = QtGui.QLCDNumber(self.OrbitGroup)
        self.num_rp.setGeometry(QtCore.QRect(40, 20, 51, 23))
        self.num_rp.setObjectName(_fromUtf8("num_rp"))
        self.label_rp = QtGui.QLabel(self.OrbitGroup)
        self.label_rp.setGeometry(QtCore.QRect(20, 10, 20, 41))
        self.label_rp.setObjectName(_fromUtf8("label_rp"))
        self.num_omega = QtGui.QLCDNumber(self.OrbitGroup)
        self.num_omega.setGeometry(QtCore.QRect(40, 60, 51, 23))
        self.num_omega.setObjectName(_fromUtf8("num_omega"))
        self.num_ra = QtGui.QLCDNumber(self.OrbitGroup)
        self.num_ra.setGeometry(QtCore.QRect(40, 40, 51, 23))
        self.num_ra.setObjectName(_fromUtf8("num_ra"))
        self.label_ra = QtGui.QLabel(self.OrbitGroup)
        self.label_ra.setGeometry(QtCore.QRect(20, 40, 20, 20))
        self.label_ra.setObjectName(_fromUtf8("label_ra"))
        self.label_omega = QtGui.QLabel(self.OrbitGroup)
        self.label_omega.setGeometry(QtCore.QRect(20, 60, 20, 20))
        self.label_omega.setObjectName(_fromUtf8("label_omega"))
        self.DebrisGroup.raise_()
        self.DebrisGroup.raise_()
        self.PositionGroup.raise_()
        self.OrbitGroup.raise_()
        self.gridLayout.addWidget(self.groupBox_2, 6, 0, 1, 3)
        spacerItem1 = QtGui.QSpacerItem(20, 36, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 5, 0, 1, 1)
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setMinimumSize(QtCore.QSize(200, 64))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(30, 20, 31, 21))
        self.label.setObjectName(_fromUtf8("label"))
        self.lineEdit = QtGui.QLineEdit(self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(70, 20, 31, 21))
        self.lineEdit.setText(_fromUtf8(""))
        self.lineEdit.setDragEnabled(False)
        self.lineEdit.setPlaceholderText(_fromUtf8(""))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.percent = QtGui.QSpinBox(self.groupBox)
        self.percent.setGeometry(QtCore.QRect(70, 40, 41, 21))
        self.percent.setWrapping(True)
        self.percent.setSuffix(_fromUtf8(""))
        self.percent.setMaximum(100)
        self.percent.setObjectName(_fromUtf8("percent"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(0, 40, 61, 21))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.percent_2 = QtGui.QSpinBox(self.groupBox)
        self.percent_2.setGeometry(QtCore.QRect(270, 20, 41, 21))
        self.percent_2.setWrapping(True)
        self.percent_2.setSuffix(_fromUtf8(""))
        self.percent_2.setMaximum(100)
        self.percent_2.setObjectName(_fromUtf8("percent_2"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(217, 20, 47, 21))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label.raise_()
        self.lineEdit.raise_()
        self.percent.raise_()
        self.label_2.raise_()
        self.percent_2.raise_()
        self.label_3.raise_()
        self.gridLayout.addWidget(self.groupBox, 4, 0, 1, 4)
        spacerItem2 = QtGui.QSpacerItem(20, 36, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 3, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 812, 27))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName(_fromUtf8("menuEdit"))
        self.menuRun = QtGui.QMenu(self.menubar)
        self.menuRun.setObjectName(_fromUtf8("menuRun"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen_file = QtGui.QAction(MainWindow)
        self.actionOpen_file.setObjectName(_fromUtf8("actionOpen_file"))
        self.actionSave_file = QtGui.QAction(MainWindow)
        self.actionSave_file.setObjectName(_fromUtf8("actionSave_file"))
        self.actionClose = QtGui.QAction(MainWindow)
        self.actionClose.setObjectName(_fromUtf8("actionClose"))
        self.actionRun = QtGui.QAction(MainWindow)
        self.actionRun.setEnabled(True)
        self.actionRun.setObjectName(_fromUtf8("actionRun"))
        self.actionFast_Forward = QtGui.QAction(MainWindow)
        self.actionFast_Forward.setObjectName(_fromUtf8("actionFast_Forward"))
        self.actionPause = QtGui.QAction(MainWindow)
        self.actionPause.setObjectName(_fromUtf8("actionPause"))
        self.actionQuick_Run = QtGui.QAction(MainWindow)
        self.actionQuick_Run.setObjectName(_fromUtf8("actionQuick_Run"))
        self.actionAdd = QtGui.QAction(MainWindow)
        self.actionAdd.setObjectName(_fromUtf8("actionAdd"))
        self.menuFile.addAction(self.actionOpen_file)
        self.menuFile.addAction(self.actionSave_file)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)
        self.menuEdit.addAction(self.actionAdd)
        self.menuRun.addAction(self.actionRun)
        self.menuRun.addAction(self.actionFast_Forward)
        self.menuRun.addAction(self.actionPause)
        self.menuRun.addSeparator()
        self.menuRun.addAction(self.actionQuick_Run)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuRun.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.laserType.setItemText(0, _translate("MainWindow", "Choose", None))
        self.laserType.setItemText(1, _translate("MainWindow", "CO2", None))
        self.laserType.setItemText(2, _translate("MainWindow", "Nd:YAG", None))
        self.laserType.setItemText(3, _translate("MainWindow", "TiS", None))
        self.laserType.setItemText(4, _translate("MainWindow", "Custom", None))
        self.label_laser.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Laser: </span></p></body></html>", None))
        self.closeBtn.setText(_translate("MainWindow", "Close", None))
        self.DebrisGroup.setTitle(_translate("MainWindow", "Debris:", None))
        self.label_etac.setText(_translate("MainWindow", "<html><head/><body><p align=\"right\"><span style=\" font-style:italic;\">η</span><span style=\" font-style:italic; vertical-align:sub;\">c </span>:</p></body></html>", None))
        self.label_Cm.setText(_translate("MainWindow", "<html><head/><body><p align=\"right\"><span style=\" font-size:10pt; font-style:italic;\">C</span><span style=\" font-size:10pt; font-style:italic; vertical-align:sub;\">m </span><span style=\" font-size:10pt;\">:</span></p></body></html>", None))
        self.label_m.setText(_translate("MainWindow", "<html><head/><body><p align=\"right\"><span style=\" font-style:italic;\">m </span>:</p></body></html>", None))
        self.label_d.setText(_translate("MainWindow", "<html><head/><body><p align=\"right\"><span style=\" font-style:italic;\">d </span>:</p></body></html>", None))
        self.PositionGroup.setTitle(_translate("MainWindow", "Position:", None))
        self.label_r.setText(_translate("MainWindow", "<html><head/><body><p align=\"right\"><span style=\" font-style:italic;\">r </span>:</p></body></html>", None))
        self.label_v.setText(_translate("MainWindow", "<html><head/><body><p align=\"right\"><span style=\" font-style:italic;\">v </span>:</p></body></html>", None))
        self.label_nu.setText(_translate("MainWindow", "<html><head/><body><p align=\"right\">ν :</p></body></html>", None))
        self.OrbitGroup.setTitle(_translate("MainWindow", "Orbit:", None))
        self.label_epsilon.setText(_translate("MainWindow", "<html><head/><body><p align=\"right\"><span style=\" font-style:italic;\">ε </span>:</p></body></html>", None))
        self.label_rp.setText(_translate("MainWindow", "<html><head/><body><p align=\"right\"><span style=\" font-style:italic;\">r</span><span style=\" font-style:italic; vertical-align:sub;\">p </span>:</p></body></html>", None))
        self.label_ra.setText(_translate("MainWindow", "<html><head/><body><p align=\"right\"><span style=\" font-style:italic;\">r</span><span style=\" font-style:italic; vertical-align:sub;\">a </span>:</p></body></html>", None))
        self.label_omega.setText(_translate("MainWindow", "<html><head/><body><p align=\"right\">𝜔 :</p></body></html>", None))
        self.groupBox.setTitle(_translate("MainWindow", "Antenna:", None))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"right\"><span style=\" font-style:italic;\">D</span> :</p></body></html>", None))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"right\">Usage :</p></body></html>", None))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p align=\"right\">Object :</p></body></html>", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit", None))
        self.menuRun.setTitle(_translate("MainWindow", "Run", None))
        self.actionOpen_file.setText(_translate("MainWindow", "Open file", None))
        self.actionSave_file.setText(_translate("MainWindow", "Save file", None))
        self.actionClose.setText(_translate("MainWindow", "Close", None))
        self.actionRun.setText(_translate("MainWindow", "Run", None))
        self.actionFast_Forward.setText(_translate("MainWindow", "Fast Forward", None))
        self.actionPause.setText(_translate("MainWindow", "Pause", None))
        self.actionQuick_Run.setText(_translate("MainWindow", "Quick Run", None))
        self.actionAdd.setText(_translate("MainWindow", "Add Debris", None))

####### GUI Operations
        self.closeBtn.clicked.connect(self.close_application)
        self.actionClose.triggered.connect(self.close_application)

        self.laserType.activated[str].connect(self.laser_choice)
#        sys.path.insert(0, './Subsystems')
#        import guiOp


    def laser_choice(self, text):
        print text
#        self.laserwidget = 

    def close_application(self):
        choice = QtGui.QMessageBox.question(self.centralwidget, "Close", "Are you sure?",
                                            QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)

        if choice == QtGui.QMessageBox.Yes:
            sys.exit()
        else:
            pass

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

