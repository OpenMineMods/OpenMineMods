from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread

from functools import partial

from API.CurseAPI import CurseFile, CurseAPI, CurseProject, CurseModpack
from API.MultiMC import MultiMCInstance, MultiMC

from GUI.NewInstanceDialog import Ui_NewInstanceDialog
from Utils.Utils import load_style_sheet


class NewInstanceDialog:
    def __init__(self, forgedat: dict):
        self.dia = QDialog()
        self.ui = Ui_NewInstanceDialog()

        self.ui.setupUi(self.dia)

        self.style = load_style_sheet('main')
        self.dia.setStyleSheet(self.style)

        for mcver in forgedat:
            self.ui.mc_ver.addItem(mcver)

        self.dia.exec_()
