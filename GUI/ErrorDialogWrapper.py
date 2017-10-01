from PyQt5.QtWidgets import *

from functools import partial

from GUI.ErrorDialog import Ui_ErrorDialog


class ErrorDialog:
    def __init__(self, exception):
        self.exc = exception
        self.win = QDialog()
        self.ui = Ui_ErrorDialog()
        self.ui.setupUi(self.win)

        self.ui.exc_info.setText(exception)

        self.ui.send_box.clicked.connect(self.toggle_details)

        self.toggle_details()

        self.ui.donebutton.clicked.connect(partial(self.win.done, 0))

        self.win.exec_()

        if self.ui.send_box.isChecked():
            self.send_crash_report()

    def toggle_details(self):
        self.ui.email_box.setHidden(not self.ui.send_box.isChecked())
        self.ui.notes_edit.setHidden(not self.ui.send_box.isChecked())

    def send_crash_report(self):
        to_send = {
            "exc_info": self.exc,
            "email": self.ui.email_box.text(),
            "notes": self.ui.notes_edit.toPlainText()
        }

        print(to_send)
