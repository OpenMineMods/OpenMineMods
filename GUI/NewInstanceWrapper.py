from PyQt5.QtWidgets import *

from GUI.NewInstanceDialog import Ui_NewInstanceDialog
from Utils.Utils import load_style_sheet


class NewInstanceDialog:
    def __init__(self, forgedat: dict):
        self.forge_data = forgedat
        self.dia = QDialog()
        self.ui = Ui_NewInstanceDialog()

        self.ui.setupUi(self.dia)

        self.style = load_style_sheet('main')
        self.dia.setStyleSheet(self.style)

        mcvers = [i for i in forgedat.keys()]
        mcvers.sort(key=lambda x: [int(i) for i in x.split(".")], reverse=True)
        for mcver in mcvers:
            self.ui.mc_ver.addItem(mcver)

        self.ui.pushButton.clicked.connect(self.create_instance)
        self.ui.mc_ver.currentIndexChanged.connect(self.mcver_changed)
        self.mcver_changed()

        self.dia.exec_()

    def create_instance(self):
        return

    def mcver_changed(self):
        self.ui.forge_ver.clear()
        nv = self.ui.mc_ver.currentText()
        forgevers = self.forge_data[nv]
        forgevers.sort(key=lambda x: [int(i) for i in x.split(".")], reverse=True)
        for forgever in forgevers:
            self.ui.forge_ver.addItem(forgever)
