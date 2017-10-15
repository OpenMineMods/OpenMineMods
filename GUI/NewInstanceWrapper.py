from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread

from functools import partial

from API.CurseAPI import CurseFile, CurseAPI, CurseProject, CurseModpack
from API.MultiMC import MultiMCInstance, MultiMC

from GUI.NewInstanceDialog import Ui_NewInstanceDialog


class NewInstanceDialog:
    def __init__(self, forgedat: dict):
        self.dia = QDialog()
        self.ui = Ui_NewInstanceDialog()

        self.ui.setupUi(self.dia)

        for mcver in forgedat:
            self.ui.mc_ver.addItem(mcver)

        self.dia.exec_()
