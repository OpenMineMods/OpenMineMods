from PyQt5.QtWidgets import *

from API.CurseAPI import CurseAPI

from requests import post

from functools import partial
from uuid import uuid4

from GUI.ErrorDialog import Ui_ErrorDialog

from Utils.Utils import msg_box, load_style_sheet


class ErrorDialog:
    def __init__(self, exception):
        self.exc = exception
        self.win = QDialog()
        self.ui = Ui_ErrorDialog()
        self.ui.setupUi(self.win)

        self.ui.exc_info.setText(exception)

        self.ui.send_box.clicked.connect(self.toggle_details)

        self.toggle_details()

        self.ui.donebutton.clicked.connect(partial(self.win.done, 1))

        self.style = load_style_sheet('main')
        self.dia.setStyleSheet(self.style)

        res = self.win.exec_()

        if self.ui.send_box.isChecked() and res:
            self.send_crash_report()

    def toggle_details(self):
        self.ui.email_box.setHidden(not self.ui.send_box.isChecked())
        self.ui.notes_edit.setHidden(not self.ui.send_box.isChecked())
        self.ui.donebutton.setText(["Quit", "Send Report"][self.ui.send_box.isChecked()])

    def send_crash_report(self):
        to_send = {
            "exc": self.exc,
            "email": self.ui.email_box.text(),
            "notes": self.ui.notes_edit.toPlainText(),
            "uuid": str(uuid4()).split("-")[0],
            "ver": CurseAPI.version
        }

        post("https://openminemods.digitalfishfun.com/analytics/crash", json=to_send)

        msg_box(None, "Your error has been recorded.\nReport ID: {}".format(to_send["uuid"]))
