from PyQt5.QtWidgets import *


def clearLayout(layout):
    for i in reversed(range(layout.count())):
        layout.itemAt(i).widget().setParent(None)


def confirmBox(parent, icon, text, default=QMessageBox.No):
    msgbox = QMessageBox(parent)
    msgbox.setIcon(icon)
    msgbox.setText(text)
    msgbox.addButton(QMessageBox.Yes)
    msgbox.addButton(QMessageBox.No)
    msgbox.setDefaultButton(QMessageBox.No)

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
