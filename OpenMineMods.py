import sys

from PyQt5.QtWidgets import *

from functools import partial
from os import path

from API.CurseAPI import CurseAPI
from API.MultiMC import MultiMC, MultiMCInstance

from Utils.Utils import dir_box, confirm_box

from GUI.MainWindow import Ui_MainWindow
from GUI.InstanceWidget import Ui_InstanceWidget


def delete_clicked(instance: MultiMCInstance):
    print(confirm_box(wg, QMessageBox.Question,
                      "Are you sure you want to delete {}".format(instance.name)))

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

for instance in mmc.instances:
    qw = QWidget()
    ie = Ui_InstanceWidget()
    ie.setupUi(qw)
    ie.instance_delete.clicked.connect(partial(delete_clicked, instance))
    ie.instance_name.setText(instance.name)
    ui.instance_box.addWidget(qw)

ui.instance_box.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
ui.mmc_folder.setText(curse.baseDir)

wg.show()
sys.exit(app.exec_())
