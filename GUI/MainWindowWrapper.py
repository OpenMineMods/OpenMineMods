from PyQt5.QtWidgets import *

from functools import partial
from os import path

from API.CurseAPI import CurseAPI
from API.MultiMC import MultiMC, MultiMCInstance

from Utils.Utils import clear_layout, confirm_box, dir_box

from GUI.MainWindow import Ui_MainWindow

from GUI.InstanceWindowWrapper import InstanceWindow

from GUI.InstanceWidget import Ui_InstanceWidget
from GUI.PackWidget import Ui_PackWidget


class MainWindow:
    def __init__(self):
        self.curse = CurseAPI()
        self.win = QMainWindow()

        while not self.curse.baseDir:
            self.curse.baseDir = dir_box(self.win, "Select Your MultiMC Folder", path.expanduser("~"))
            self.curse.db["baseDir"] = self.curse.baseDir

        self.mmc = MultiMC(self.curse.baseDir)

        self.children = list()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.win)

        self.win.setWindowTitle("OpenMineMods v{}".format(self.curse.version))

        self.init_instances()
        self.init_packs()

        self.ui.mmc_folder.setText(self.curse.baseDir)
        self.ui.analytics_check.setChecked(self.curse.db["analytics"])
        self.ui.analytics_check.clicked.connect(self.analytics_checked)

        self.win.show()

    """UI Initializations"""

    def init_instances(self):
        clear_layout(self.ui.instance_box)

        for instance in self.mmc.instances:
            widget = QWidget()
            el = Ui_InstanceWidget()

            el.setupUi(widget)

            el.instance_delete.clicked.connect(partial(self.delete_clicked, instance))
            el.instance_edit.clicked.connect(partial(self.edit_clicked, instance))

            el.instance_name.setText(instance.name)

            self.ui.instance_box.addWidget(widget)

        self.ui.instance_box.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def init_packs(self):
        clear_layout(self.ui.pack_box)

        for pack in ["Test", "Test1"] * 20:
            widget = QWidget()
            el = Ui_PackWidget()

            el.setupUi(widget)

            el.pack_name.setText(pack)

            self.ui.pack_box.addWidget(widget)

        self.ui.pack_box.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    """Event Listeners"""

    def delete_clicked(self, instance: MultiMCInstance):
        print(confirm_box(self.win, QMessageBox.Question,
                          "Are you sure you want to delete {}".format(instance.name)))

    def edit_clicked(self, instance: MultiMCInstance):
        self.children.append(InstanceWindow(instance))

    def analytics_checked(self):
        self.curse.db["analytics"] = self.ui.analytics_check.isChecked()
