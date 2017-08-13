import sys

from PyQt5.QtWidgets import *
from CurseAPI import CurseAPI, CurseProject, SearchType
from MultiMC import MultiMC, MultiMCInstance
from functools import partial
from Utils import clearLayout, confirmBox

from PackBrowser import PackBrowseWindow
from ModBrowser import ModBrowseWindow


class AppWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.curse = CurseAPI()
        self.mmc = MultiMC(self.curse.baseDir)

        self.setWindowTitle("OpenMineMods v{}".format(CurseAPI.version))

        self.layout = QVBoxLayout(self)

        self.hGroupBox = QGroupBox("Instances")
        self.layout.addWidget(self.hGroupBox)

        self.instanceTable = QGridLayout()

        self.init_instances()

        self.hGroupBox.setLayout(self.instanceTable)

        scroll = QScrollArea()
        scroll.setWidget(self.hGroupBox)
        scroll.setWidgetResizable(True)
        self.layout.addWidget(scroll)

        brButton = QPushButton("Browse", self)
        brButton.clicked.connect(self.browse_clicked)
        self.layout.addWidget(brButton)

        self.show()

    def init_instances(self):
        clearLayout(self.instanceTable)

        for x, instance in enumerate(self.mmc.instances):
            editButton = QPushButton("Edit", self)
            editButton.clicked.connect(partial(self.edit_clicked, instance=instance))
            deleteButton = QPushButton("Delete", self)
            deleteButton.clicked.connect(partial(self.delete_clicked, instance=instance))
            self.instanceTable.addWidget(QLabel("{} (Minecraft {})".format(instance.name, instance.version)), x, 0)
            self.instanceTable.addWidget(editButton, x, 1)
            self.instanceTable.addWidget(deleteButton, x, 2)

    def edit_clicked(self, instance):
        InstanceEditWindow(self.curse, instance)

    def delete_clicked(self, instance: MultiMCInstance):
        if not confirmBox(self, QMessageBox.Warning,
                          "Are you sure you want to delete {}?".format(instance.name)):
            return
        self.mmc.delete_instance(instance)
        self.init_instances()

    def browse_clicked(self):
        PackBrowseWindow(self.curse, self.mmc, self)


class InstanceEditWindow(QWidget):
    def __init__(self, curse: CurseAPI, instance: MultiMCInstance):
        super().__init__()

        self.curse = curse
        self.instance = instance

        self.setWindowTitle("Editing {}".format(self.instance.name))

        self.layout = QVBoxLayout(self)

        self.instanceMetaBox = QGroupBox("Installed Mods")
        self.layout.addWidget(self.instanceMetaBox)

        brButton = QPushButton("Browse Mods")
        brButton.clicked.connect(partial(self.browse_clicked))
        self.layout.addWidget(brButton)

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

    def init_mods(self):
        clearLayout(self.instanceTable)

        for x, mod in enumerate(self.instance.mods):
            rmButton = QPushButton("Remove", self)
            rmButton.clicked.connect(partial(self.delete_clicked, mod=mod.filename))
            self.instanceTable.addWidget(QLabel(mod.name), x, 0)
            self.instanceTable.addWidget(rmButton, x, 1)


app = QApplication(sys.argv)
win2 = AppWindow()
sys.exit(app.exec_())
