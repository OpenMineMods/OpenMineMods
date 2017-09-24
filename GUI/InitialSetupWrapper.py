from PyQt5.QtWidgets import *

from os import path

from Utils.Config import Config, Setting

from GUI.SetupDialog import Ui_SetupDialog


class SetupWindow:
    def __init__(self, config_folder: str):
        self.conf = Config(config_folder)
        self.win = QDialog()
        self.ui = Ui_SetupDialog()
        self.ui.setupUi(self.win)

        self.mmc_folder = ""

        self.ui.tabWidget.setTabEnabled(2, False)
        self.ui.pushButton.clicked.connect(self.next_tab)
        self.ui.pushButton_2.clicked.connect(self.next_tab)

        self.ui.mmc_folder.textChanged.connect(self.folder_changed)

    def next_tab(self):
        ind = self.ui.tabWidget.currentIndex()
        if ind == 1:
            self.write_config()
            self.ui.tabWidget.setTabEnabled(0, False)
            self.ui.tabWidget.setTabEnabled(1, False)
        self.ui.tabWidget.setTabEnabled(ind + 1, True)
        self.ui.tabWidget.setCurrentIndex(ind + 1)

    def folder_changed(self):
        mmc_folder = self.ui.mmc_folder.text()
        self.mmc_folder = path.expanduser(mmc_folder)
        if path.isfile(path.join(self.mmc_folder, "multimc.cfg")):
            self.ui.pushButton_2.setEnabled(True)
        else:
            self.ui.pushButton_2.setEnabled(False)

    def write_config(self):
        self.conf.write(Setting.analytics, self.ui.analytics.isChecked())
        self.conf.write(Setting.update, self.ui.autoupdate.isChecked())

        self.conf.write(Setting.location, self.mmc_folder)
