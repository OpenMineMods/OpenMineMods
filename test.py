import sys

from PyQt5.QtWidgets import *

from GUI.InitialSetupWrapper import SetupWindow

app = QApplication(sys.argv)
win = SetupWindow(".")

win.win.exec_()

print(sys.argv)
if len(sys.argv) > 1 and sys.argv[1] == "--test":
    sys.exit(0)

#sys.exit(app.exec_())
