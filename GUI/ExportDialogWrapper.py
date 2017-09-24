from PyQt5.QtWidgets import *

from os import path, listdir

from API.MultiMC import MultiMCInstance
from API.CurseAPI import CurseAPI

from GUI.ExportDialog import Ui_ExportDialog

from GUI.ExportWidget import Ui_ExportWidget


default_selected = [
    "config",
    "mods",
    "resources",
    "scripts"
]


class ExportDialog:
    def __init__(self, instance: MultiMCInstance, curse: CurseAPI):
        self.dia = QDialog()
        self.ui = Ui_ExportDialog()
        self.ui.setupUi(self.dia)
        self.widgets = list()

        self.dia.setWindowTitle("Exporting {}".format(instance.name))

        for file in listdir(path.join(instance.path, "minecraft")):
            widget = QWidget()
            el = Ui_ExportWidget()
            el.setupUi(widget)

            el.label.setText(file)
            el.checkBox.setChecked(file in default_selected)

            self.widgets.append(el)
            self.ui.folder_layout.addWidget(widget)

        self.ui.folder_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.dia.exec_()
