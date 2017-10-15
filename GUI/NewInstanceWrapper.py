from PyQt5.QtWidgets import *

from os import path, makedirs

from API.MultiMC import InstanceCfg, ForgePatch

from GUI.NewInstanceDialog import Ui_NewInstanceDialog
from Utils.Utils import load_style_sheet


class NewInstanceDialog:
    def __init__(self, forgedat: dict, mmc_dir: str):
        self.forge_data = forgedat
        self.mmc_dir = path.join(mmc_dir, "instances")
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
        mc_ver = self.ui.mc_ver.currentText()
        forge_ver = self.ui.forge_ver.currentText()
        name = self.ui.inst_name.text()

        folder = path.join(self.mmc_dir, name)

        while path.exists(folder):
            folder += "_"

        makedirs(folder)
        makedirs(path.join(folder, "patches"))

        instancecfg = InstanceCfg(mc_ver, forge_ver, name)
        instancecfg.write(path.join(folder, "instance.cfg"))

        patch = ForgePatch(mc_ver, forge_ver)
        patch.write(path.join(folder, "patches", "net.minecraftforge.json"))

        self.dia.done(1)

    def mcver_changed(self):
        self.ui.forge_ver.clear()
        nv = self.ui.mc_ver.currentText()
        forgevers = self.forge_data[nv]
        forgevers.sort(key=lambda x: [int(i) for i in x.split(".")], reverse=True)
        for forgever in forgevers:
            self.ui.forge_ver.addItem(forgever)
