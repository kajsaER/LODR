from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys, threading, random

qtCreatorMain = "CloseThread.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorMain)

myKillReason = 20

class OperatorGUI(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(OperatorGUI, self).__init__(parent)
        self.setupUi(self)

        self.running = False
        self.kill_reason = None
        self.lock = threading.Lock()

        self.runBtn.clicked.connect(self.run_pushed)

    def run_pushed(self):
        self.running = not self.running
        if self.running:
            self.thread_1 = threading.Thread(target=self.myThread).start()
        else:
            self.label.setText("Not Running")

    def myThread(self):
        self.kill_reason = None
        self.label.setText("Running")
        while self.running:
            self.lock.acquire()
            num = random.random()

            if num > 0.99999999:
                self.kill_reason = myKillReason
                self.running = False

            self.lock.release()

        if self.kill_reason == myKillReason:
            self.label.setText("Not Running")
            QtWidgets.QMessageBox.information(None, "Error", "Random value above limit",
                                              QtWidgets.QMessageBox.Ok)


if __name__ == "__main__":
    sys.settrace
    app = QtWidgets.QApplication(sys.argv)
    window = OperatorGUI()
    window.show()
    sys.exit(app.exec_())
