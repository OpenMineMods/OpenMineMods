import sys
import Logger

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import *
from CurseAPI import CurseAPI
from MultiMC import MultiMC, MultiMCInstance
from functools import partial
from Utils import clearLayout, confirmBox, directoryBox, makeIconButton
from Analytics import send_data
from pickle import UnpicklingError

from PackBrowser import PackBrowseWindow
from ModBrowser import ModBrowseWindow


class AppWindow(QWidget):
    def __init__(self):
        super().__init__()

        try:
            self.curse = CurseAPI()
        except UnpicklingError:
            self.layout = QVBoxLayout(self)
            Logger.err("Unable to read DB")
            self.setWindowTitle("ERROR")
            self.layout.addWidget(QLabel("There was an error loading the database.\nPlease delete `omm.db*` from your home directory and try again."))

        if not self.curse.baseDir:
            self.curse.baseDir = directoryBox(self, "Please select your MultiMC folder")
            self.curse.db["baseDir"] = self.curse.baseDir

        Logger.info("MultiMC folder is {}".format(self.curse.baseDir))

        if "analytics" not in self.curse.db:
            self.curse.db["analytics"] = confirmBox(self, QMessageBox.Question, "Enable basic analytics?")
            if self.curse.db["analytics"]:
                send_data(self.curse)

        self.analytics = self.curse.db["analytics"]

        Logger.info("Analytics are {}".format(["Disabled", "Enabled"][self.analytics]))

        self.mmc = MultiMC(self.curse.baseDir)

        self.setWindowTitle("OpenMineMods v{}".format(CurseAPI.version))

        self.layout = QVBoxLayout(self)
        # Start Buttons
        self.buttonGroup = QGroupBox()
        self.layoutButtons = QHBoxLayout()
        self.buttonGroup.setLayout(self.layoutButtons)
        self.buttonGroup.setStyleSheet("QGroupBox { border:0; } ")

        refreshInstances = makeIconButton(self, "refresh", "Refresh Instances")
        refreshInstances.clicked.connect(self.refresh_instances)

        brButton = makeIconButton(self, "search", "Browse Modpacks")
        brButton.clicked.connect(self.browse_clicked)

        settingsButton = makeIconButton(self, "configure", "Configure OpenMineMods")

        self.layoutButtons.setAlignment(Qt.AlignTop)
        self.layoutButtons.addWidget(refreshInstances)
        self.layoutButtons.addWidget(brButton)
        self.layoutButtons.addWidget(settingsButton)
        self.layoutButtons.addStretch(1)
        self.layoutButtons.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.buttonGroup)
        # End Buttons
        self.hGroupBox = QGroupBox("Instances")
        self.layout.addWidget(self.hGroupBox)

        self.instanceTable = QVBoxLayout()

        self.init_instances()

        self.hGroupBox.setLayout(self.instanceTable)

        scroll = QScrollArea()
        scroll.setWidget(self.hGroupBox)
        scroll.setWidgetResizable(True)
        self.layout.addWidget(scroll)

        self.show()

    def refresh_instances(self):
        self.mmc = MultiMC(self.curse.baseDir, self.mmc.metaDb)
        self.init_instances()

    def init_instances(self):
        clearLayout(self.instanceTable)

        def create_instance_item(instance):
            group = QGroupBox(self)
            hbox = QHBoxLayout()
            group.setLayout(hbox)
            group.setStyleSheet("QGroupBox { border:0; } ")

            editButton = makeIconButton(self, "edit", "Edit Instance")
            editButton.clicked.connect(partial(self.edit_clicked, instance=instance))

            deleteButton = makeIconButton(self, "edit-delete", "Delete Instance")
            deleteButton.clicked.connect(partial(self.delete_clicked, instance=instance))

            hbox.addStretch(1)
            hbox.addWidget(QLabel("{} (Minecraft {})".format(instance.name, instance.version)))
            hbox.addWidget(editButton)
            hbox.addWidget(deleteButton)

            return group

        for instance in self.mmc.instances:
            self.instanceTable.addWidget(create_instance_item(instance))

    def edit_clicked(self, instance):
        InstanceEditWindow(self.curse, instance)

    def delete_clicked(self, instance: MultiMCInstance):
        if not confirmBox(self, QMessageBox.Warning,
                          "Are you sure you want to delete {}?".format(instance.name)):
            return
        self.mmc.delete_instance(instance)
        self.init_instances()

    def browse_clicked(self):
        PackBrowseWindow(self.curse, self.mmc)


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
            rmButton = makeIconButton(self, "edit-delete", "Remove Mod")
            rmButton.clicked.connect(partial(self.delete_clicked, mod=mod.file.filename))

            self.instanceTable.addWidget(QLabel(mod.file.name), x, 0)
            self.instanceTable.addWidget(rmButton, x, 1)


def main():
    app = QApplication(sys.argv)
    win2 = AppWindow()
    sys.exit(app.exec_())


main()
