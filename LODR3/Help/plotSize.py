import sys

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt4 import QtCore, QtGui, uic

qtCreatorMain = "GUI.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorMain)

class MainGUI(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainGUI, self).__init__(parent)
        self.setupUi(self)

        #### Lots of other code goes here ####

        # PlotView
        self.figure = Figure()
#        self.figure.set_size_inches(2, 5)
        self.canvas = FigureCanvas(self.figure)
#        self.canvas.setGeometry(0, 0, 500, 1000)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.plotLayout.addWidget(self.toolbar)
        self.plotLayout.addWidget(self.canvas)
        pl = self.figure.add_subplot(111)


        ### Even more code goes here ####

if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    window = MainGUI()
    window.show()
    sys.exit(app.exec_())
