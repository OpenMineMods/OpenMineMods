from PyQt5.QtWidgets import *

from os import path

from GUI.SetupDialog import Ui_SetupDialog


class SetupWindow:
    def __init__(self):
        self.win = QDialog()
        self.ui = Ui_SetupDialog()
        self.ui.setupUi(self.win)

        self.ui.tabWidget.setTabEnabled(2, False)
        self.ui.pushButton.clicked.connect(self.next_tab)
        self.ui.pushButton_2.clicked.connect(self.next_tab)

        self.ui.mmc_folder.textChanged.connect(self.folder_changed)

    def next_tab(self):
        ind = self.ui.tabWidget.currentIndex()
        self.ui.tabWidget.setTabEnabled(ind + 1, True)
        self.ui.tabWidget.setCurrentIndex(ind + 1)

    def folder_changed(self):
        mmc_folder = self.ui.mmc_folder.text()
        mmc_folder = path.expanduser(mmc_folder)
        if path.isdir(mmc_folder) and path.exists(path.join(mmc_folder, "multimc.cfg")):
            self.ui.pushButton_2.setEnabled(True)
        else:
            self.ui.pushButton_2.setEnabled(False)
