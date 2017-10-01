#!/usr/bin/env python3

import sys

from Utils.ErrorHandler import handle_exception

from PyQt5.QtWidgets import *

from GUI.MainWindowWrapper import MainWindow


sys.excepthook = handle_exception

app = QApplication(sys.argv)
win = MainWindow()

if len(sys.argv) > 1 and sys.argv[1] == "--test":
    sys.exit(0)

sys.exit(app.exec_())
