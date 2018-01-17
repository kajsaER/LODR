import sys

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.patches import Circle as Circle
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
        self.figure = Figure(tight_layout=True)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.plotLayout.addWidget(self.toolbar)
        self.plotLayout.addWidget(self.canvas)
        self.graph = self.figure.add_subplot(111)
        self.graph.add_patch(Circle((0,0), 3, color='b', alpha=0.5))
        self.graph.axis('equal')
        
        self.graph.plot([-3, -2, -1, 0, 1, 2, 3], [0, -1, 4, 2, 0, -3, -5])
        self.graph.plot(0, 0, '*')

        ### Even more code goes here ####

if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    window = MainGUI()
    window.show()
    sys.exit(app.exec_())
