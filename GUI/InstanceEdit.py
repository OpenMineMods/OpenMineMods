from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from API.CurseAPI import CurseAPI
from API.MultiMC import MultiMCInstance
from functools import partial
from Utils.Utils import clearLayout, makeIconButton

from GUI.Strings import Strings

from GUI.ModBrowser import ModBrowseWindow

strings = Strings()
translate = strings.get


class InstanceEditWindow(QWidget):
    def __init__(self, curse: CurseAPI, instance: MultiMCInstance):
        super().__init__()

        self.curse = curse
        self.instance = instance

        self.setWindowTitle(translate("title.editing").format(self.instance.name))

        self.layout = QVBoxLayout(self)

        self.instanceMetaBox = QGroupBox(translate("label.installed"))
        self.layout.addWidget(self.instanceMetaBox)

        self.buttonGroup = QGroupBox()
        self.layoutButtons = QHBoxLayout()
        self.buttonGroup.setLayout(self.layoutButtons)
        self.buttonGroup.setStyleSheet("QGroupBox { border:0; } ")

        self.brButton = makeIconButton(self, "search", translate("tooltip.browse.mods"))
        self.brButton.clicked.connect(self.browse_clicked)
        self.layoutButtons.addWidget(self.brButton)

        self.ucButton = makeIconButton(self, "view-refresh", translate("tooltip.update.check"))
        self.ucButton.clicked.connect(self.update_check_clicked)
        self.layoutButtons.addWidget(self.ucButton)

        self.layout.addWidget(self.buttonGroup)

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

    def update_check_clicked(self):
        self.ucButton.setIcon(QIcon("Assets/software-update-available-symbolic.svg"))
        self.ucButton.setToolTip(translate("tooltip.update.install"))

    def init_mods(self):
        clearLayout(self.instanceTable)

        for x, mod in enumerate(self.instance.mods):
            rmButton = makeIconButton(self, "edit-delete", translate("tooltip.delete.mod"))
            rmButton.clicked.connect(partial(self.delete_clicked, mod=mod.file.filename))

            self.instanceTable.addWidget(QLabel(mod.file.name), x, 0)
            self.instanceTable.addWidget(rmButton, x, 1)