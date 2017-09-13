import os

from os import path
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


def parseSemanticVersion(ver: str):
    return tuple([int(i) for i in ver.split(".")])


def getVersionString(ver: tuple):
    return ".".join([str(i) for i in ver])


def getInstallDir():
    return path.dirname(path.dirname(path.realpath(__file__)))


def moveTree(sourceRoot, destRoot):
    if not os.path.exists(destRoot):
        return False
    ok = True
    for path, dirs, files in os.walk(sourceRoot):
        relPath = os.path.relpath(path, sourceRoot)
        destPath = os.path.join(destRoot, relPath)
        if not os.path.exists(destPath):
            os.makedirs(destPath)
        for file in files:
            destFile = os.path.join(destPath, file)
            srcFile = os.path.join(path, file)
            os.rename(srcFile, destFile)
    for path, dirs, files in os.walk(sourceRoot, False):
        if len(files) == 0 and len(dirs) == 0:
            os.rmdir(path)
    return ok
