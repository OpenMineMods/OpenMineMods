from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize


def clearLayout(layout):
    for i in reversed(range(layout.count())):
        layout.itemAt(i).widget().setParent(None)


def confirmBox(parent, icon, text, default=QMessageBox.No):
    msgbox = QMessageBox(parent)
    msgbox.setIcon(icon)
    msgbox.setText(text)
    msgbox.addButton(QMessageBox.Yes)
    msgbox.addButton(QMessageBox.No)
    msgbox.setDefaultButton(default)

    return msgbox.exec_() == QMessageBox.Yes


def msgBox(parent=False, icon=QMessageBox.Information, text="Someone forgot to set this..."):
    if parent:
        msgbox = QMessageBox(parent)
    else:
        msgbox = QMessageBox()
    msgbox.setIcon(icon)
    msgbox.setText(text)
    msgbox.addButton(QMessageBox.Ok)
    msgbox.setDefaultButton(QMessageBox.Ok)

    msgbox.exec_()


def directoryBox(parent, text):
    return QFileDialog.getExistingDirectory(parent, text)


def makeIconButton(parent, icon, text):
    button = QPushButton(parent)
    button.setIcon(QIcon("Assets/{}.svg".format(icon)))
    button.setIconSize(QSize(24, 24))
    button.setToolTip(text)
    return button
