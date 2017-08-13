import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot
from CurseAPI import CurseAPI
from MultiMC import MultiMC, MultiMCInstance
from functools import partial


def confirmBox(parent, icon, text):
    msgbox = QMessageBox(parent)
    msgbox.setIcon(icon)
    msgbox.setText(text)
    msgbox.addButton(QMessageBox.Yes)
    msgbox.addButton(QMessageBox.No)
    msgbox.setDefaultButton(QMessageBox.No)

    return msgbox.exec_() == QMessageBox.Yes


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.curse = CurseAPI()
        self.mmc = MultiMC(self.curse.baseDir)

        self.setWindowTitle("OpenMineMods v{}".format(CurseAPI.version))

        self.layout = QVBoxLayout()

        self.hGroupBox = QGroupBox("Instances")
        self.layout.addWidget(self.hGroupBox)

        self.instanceTable = QGridLayout()

        for x, instance in enumerate(self.mmc.instances):
            editButton = QPushButton("Edit", self)
            editButton.clicked.connect(partial(self.edit_clicked, instance=instance))
            deleteButton = QPushButton("Delete", self)
            deleteButton.clicked.connect(partial(self.delete_clicked, instance=instance))
            self.instanceTable.addWidget(QLabel(instance.name), x, 0)
            self.instanceTable.addWidget(QLabel(instance.version), x, 1)
            self.instanceTable.addWidget(editButton, x, 2)
            self.instanceTable.addWidget(deleteButton, x, 3)

        self.hGroupBox.setLayout(self.instanceTable)
        self.setLayout(self.layout)

        self.show()

    @pyqtSlot()
    def edit_clicked(self, instance: MultiMCInstance):
        print(instance.name)

    @pyqtSlot()
    def delete_clicked(self, instance: MultiMCInstance):
        if not confirmBox(self, QMessageBox.Warning,
                          "Are you sure you want to delete {}?".format(instance.name)):
            return
        print("DELETE TEH INSTANCE")


app = QApplication(sys.argv)

win = MainWindow()

sys.exit(app.exec_())
