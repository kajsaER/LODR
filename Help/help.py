import sys
from PyQt4 import QtCore, QtGui, uic

Main = "Main.ui"
MainUI, MainBase = uic.loadUiType(Main)
Text = "textwidget.ui"
TWidget, TBase = uic.loadUiType(Text)
Cal = "calendarwidget.ui"
CWidget, CBase = uic.loadUiType(Cal)

class OperatorGUI(MainBase, MainUI):
    def __init__(self, parent=None):
        super(OperatorGUI, self).__init__(parent)
        self.setupUi(self)
        self.comboBox.activated[str].connect(self.choose_widget)

        self.ChangingWidget.setLayout(QtGui.QVBoxLayout())
        self.stacked = QtGui.QStackedWidget()
        self.ChangingWidget.layout().addWidget(self.stacked)
        self.textWidget = TextWidget()
        self.calendarWidget = CalendarWidget()
        self.stacked.addWidget(self.textWidget)
        self.stacked.addWidget(self.calendarWidget)


    def choose_widget(self, choice):
        # Set the widget accorging to the choice
        if choice == "Option 1":
            self.stacked.setCurrentWidget(self.textWidget)
        elif choice == "Option 2":
            self.stacked.setCurrentWidget(self.calendarWidget)
        print choice
        self.stacked.currentWidget().show()
#        self.setupUi(self)
        self.show()
        

class TextWidget(TBase, TWidget):
    def __init__(self, parent=None):
        super(TextWidget, self).__init__(parent)
#        self.setParent(parent)
        self.setupUi(self)
        print "Text"

class CalendarWidget(CBase, CWidget):
    def __init__(self, parent=None):
        super(CalendarWidget, self).__init__(parent)
#        self.setParent(parent)
        self.setupUi(self)
        print "Calendar"


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = OperatorGUI()
    window.show()
    sys.exit(app.exec_())
