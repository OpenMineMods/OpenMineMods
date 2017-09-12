import sys
import Utils.Logger as Logger

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from API.CurseAPI import CurseAPI
from API.MultiMC import MultiMC, MultiMCInstance
from functools import partial
from Utils.Utils import clearLayout, confirmBox, directoryBox, makeIconButton
from Utils.Analytics import send_data

from GUI.Strings import Strings

from GUI.PackBrowser import PackBrowseWindow
from GUI.Setting import SettingsWindow
from GUI.InstanceEdit import InstanceEditWindow

strings = Strings()
translate = strings.get


class AppWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.curse = CurseAPI()

        if not self.curse.baseDir:
            self.curse.baseDir = directoryBox(self, translate("prompt.mmc"))
            if not self.curse.baseDir:
                exit(1)
            self.curse.db["baseDir"] = self.curse.baseDir

        Logger.info("MultiMC folder is {}".format(self.curse.baseDir))

        if "analytics" not in self.curse.db:
            self.curse.db["analytics"] = confirmBox(self, QMessageBox.Question,
                                                    translate("prompt.analytics"), QMessageBox.Yes)
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

        refreshInstances = makeIconButton(self, "view-refresh", translate("tooltip.refresh.instances"))
        refreshInstances.clicked.connect(self.refresh_instances)

        brButton = makeIconButton(self, "search", "Browse Modpacks")
        brButton.clicked.connect(self.browse_clicked)

        settingsButton = makeIconButton(self, "configure", translate("tooltip.configure.omm"))
        settingsButton.clicked.connect(self.settings_clicked)

        self.layoutButtons.setAlignment(Qt.AlignTop)
        self.layoutButtons.addWidget(refreshInstances)
        self.layoutButtons.addWidget(brButton)
        self.layoutButtons.addWidget(settingsButton)
        self.layoutButtons.addStretch(1)
        self.layoutButtons.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.buttonGroup)
        # End Buttons
        self.hGroupBox = QGroupBox(translate("label.instances"))
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

            editButton = makeIconButton(self, "edit", translate("tooltip.edit.instance"))
            editButton.clicked.connect(partial(self.edit_clicked, instance=instance))

            deleteButton = makeIconButton(self, "edit-delete", translate("tooltip.delete.instance"))
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
        if not confirmBox(self, QMessageBox.Warning, translate("prompt.delete").format(instance.name)):
            return
        self.mmc.delete_instance(instance)
        self.init_instances()

    def browse_clicked(self):
        PackBrowseWindow(self.curse, self.mmc)

    def settings_clicked(self):
        SettingsWindow(self.curse)


app = QApplication(sys.argv)
win = AppWindow()
sys.exit(app.exec_())
