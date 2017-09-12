from PyQt5.QtWidgets import *
from API.CurseAPI import CurseAPI
from API.MultiMC import MultiMCInstance
from functools import partial
from Utils.Utils import clearLayout, makeIconButton

from GUI.ModBrowser import ModBrowseWindow

class InstanceEditWindow(QWidget):
    def __init__(self, curse: CurseAPI, instance: MultiMCInstance):
        super().__init__()

        self.curse = curse
        self.instance = instance

        self.setWindowTitle("Editing {}".format(self.instance.name))

        self.layout = QVBoxLayout(self)

        self.instanceMetaBox = QGroupBox("Installed Mods")
        self.layout.addWidget(self.instanceMetaBox)

        brButton = QPushButton("Browse Mods")
        brButton.clicked.connect(partial(self.browse_clicked))
        self.layout.addWidget(brButton)

        self.instanceTable = QGridLayout()

        self.init_mods()

        self.instanceMetaBox.setLayout(self.instanceTable)

        scroll = QScrollArea()
        scroll.setWidget(self.instanceMetaBox)
        scroll.setWidgetResizable(True)
        self.layout.addWidget(scroll)

        self.show()

    def delete_clicked(self, mod: str):
        self.instance.uninstall_mod(mod)
        self.init_mods()

    def browse_clicked(self):
        ModBrowseWindow(self.curse, self.instance, self)

    def init_mods(self):
        clearLayout(self.instanceTable)

        for x, mod in enumerate(self.instance.mods):
            rmButton = makeIconButton(self, "edit-delete", "Remove Mod")
            rmButton.clicked.connect(partial(self.delete_clicked, mod=mod.file.filename))

            self.instanceTable.addWidget(QLabel(mod.file.name), x, 0)
            self.instanceTable.addWidget(rmButton, x, 1)