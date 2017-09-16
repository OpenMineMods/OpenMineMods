import sys

from PyQt5.QtWidgets import *

from functools import partial
from os import path

from API.CurseAPI import CurseAPI
from API.MultiMC import MultiMC, MultiMCInstance

from Utils.Utils import dir_box, confirm_box, clear_layout

from GUI.MainWindow import Ui_MainWindow
from GUI.InstanceWidget import Ui_InstanceWidget
from GUI.PackWidget import Ui_PackWidget

"""FUNCTION DECLARATIONS"""


def init_instances():
    clear_layout(ui.instance_box)

    for instance in mmc.instances:
        widget = QWidget()
        el = Ui_InstanceWidget()

        el.setupUi(widget)

        el.instance_delete.clicked.connect(partial(delete_clicked, instance))
        el.instance_name.setText(instance.name)

        ui.instance_box.addWidget(widget)

    ui.instance_box.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))


def init_packs():
    clear_layout(ui.pack_box)

    for pack in ["Test", "Test1"]:
        widget = QWidget()
        el = Ui_PackWidget()

        el.setupUi(widget)

        el.pack_name.setText(pack)

        ui.pack_box.addWidget(widget)

    ui.pack_box.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))


def delete_clicked(instance: MultiMCInstance):
    print(confirm_box(wg, QMessageBox.Question,
                      "Are you sure you want to delete {}".format(instance.name)))

"""INITIALIZATION"""

app = QApplication(sys.argv)
wg = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(wg)

curse = CurseAPI()

wg.setWindowTitle("OpenMineMods v{}".format(curse.version))

while not curse.baseDir:
    curse.baseDir = dir_box(wg, "Select Your MultiMC Folder", path.expanduser("~"))

curse.db["baseDir"] = curse.baseDir

mmc = MultiMC(curse.baseDir)

init_instances()
init_packs()
ui.mmc_folder.setText(curse.baseDir)

wg.show()
sys.exit(app.exec_())
