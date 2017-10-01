from PyQt5.QtWidgets import *

from functools import partial

from GUI.ErrorDialog import Ui_ErrorDialog


class ErrorDialog:
    def __init__(self, exception):
        self.win = QDialog()
        self.ui = Ui_ErrorDialog()
        self.ui.setupUi(self.win)

        self.ui.exc_info.setText(exception)

        self.ui.donebutton.clicked.connect(partial(self.win.done, 0))

        self.win.exec_()

        if self.ui.send_box.isChecked():
            print("Sending crash report...")
