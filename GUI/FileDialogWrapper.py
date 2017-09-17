from PyQt5.QtWidgets import *

from functools import partial

from GUI.FileDialog import Ui_FileDialog

from GUI.FileWidget import Ui_FileWidget


class FileDialog:
    def __init__(self, files: list):
        self.dia = QDialog()
        self.ui = Ui_FileDialog()
        self.ui.setupUi(self.dia)

        for x, f in enumerate(files):
            widget = QWidget()
            el = Ui_FileWidget()
            el.setupUi(widget)

            el.file_name.setText(f.filename)
            el.install_button.clicked.connect(partial(self.dia.done, x + 1))

            self.ui.file_box.addWidget(widget)

        self.ui.file_box.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
