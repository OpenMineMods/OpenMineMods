from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from API.CurseAPI import CurseAPI
from functools import partial
from Utils.Utils import makeIconButton, directoryBox, msgBox


class SettingsWindow(QWidget):
    def __init__(self, curse: CurseAPI):
        super().__init__()

        self.curse = curse

        self.setWindowTitle("OpenMineMods Settings")

        self.layout = QVBoxLayout(self)

        mmc_box = QGroupBox("MultiMC Location")
        mmc_layout = QHBoxLayout()

        mmc_box.setLayout(mmc_layout)

        self.mmcDir = QLineEdit(self.curse.baseDir)
        self.mmcDir.setReadOnly(True)
        self.mmcDir.setMinimumWidth(250)
        mmc_layout.addWidget(self.mmcDir, 0, Qt.AlignLeft)

        self.mmcEb = makeIconButton(self, "edit", "Change Install Location")
        self.mmcEb.clicked.connect(partial(self.browse_clicked))
        mmc_layout.addWidget(self.mmcEb, 0, Qt.AlignRight)

        self.layout.addWidget(mmc_box)

        analytics_box = QGroupBox("Analytics")
        analytics_layout = QHBoxLayout()

        analytics_box.setLayout(analytics_layout)

        self.analyticsToggle = QCheckBox()
        self.analyticsToggle.setChecked(self.curse.db["analytics"])
        self.analyticsToggle.stateChanged.connect(self.analytics_toggle)
        analytics_layout.addWidget(self.analyticsToggle, 1, Qt.AlignCenter)

        self.layout.addWidget(analytics_box)

        self.show()

    def browse_clicked(self):
        newBase = directoryBox(self, "Please select your MultiMC folder")
        if newBase:
            self.curse.baseDir = newBase
            self.curse.db["baseDir"] = newBase
            msgBox(self, QMessageBox.Information, "MultiMC folder updated!\nA restart is required for changes to take effect.")

    def analytics_toggle(self):
        new = bool(self.analyticsToggle.checkState())
        self.curse.db["analytics"] = new
