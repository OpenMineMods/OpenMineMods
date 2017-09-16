import sys

from PyQt5.QtWidgets import *

from GUI.MainWindowWrapper import MainWindow


app = QApplication(sys.argv)
win = MainWindow()
sys.exit(app.exec_())
