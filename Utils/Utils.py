import os
import zipfile

from os import path
from sys import executable
from PyQt5.QtWidgets import *


def clear_layout(layout: QLayout):
    for i in reversed(range(layout.count())):
        if layout.itemAt(i).widget() is not None:
            layout.itemAt(i).widget().setParent(None)
        if layout.itemAt(i) is not None and layout.itemAt(i).spacerItem() is not None:
            layout.removeItem(layout.itemAt(i).spacerItem())


def confirm_box(parent: QWidget, icon: int, text: str, default=QMessageBox.No):
    msgbox = QMessageBox(parent)
    msgbox.setWindowTitle(parent.windowTitle())
    msgbox.setIcon(icon)
    msgbox.setText(text)
    msgbox.addButton(QMessageBox.Yes)
    msgbox.addButton(QMessageBox.No)
    msgbox.setDefaultButton(default)

    return msgbox.exec_() == QMessageBox.Yes


def msg_box(parent: QWidget, text: str, icon=QMessageBox.Information):
    if parent:
        msgbox = QMessageBox(parent)
    else:
        msgbox = QMessageBox()
    msgbox.setIcon(icon)
    msgbox.setText(text)
    msgbox.addButton(QMessageBox.Ok)
    msgbox.setDefaultButton(QMessageBox.Ok)

    msgbox.exec_()


def dir_box(parent: QWidget, text: str, de_dir=""):
    fd = QFileDialog(parent)
    fd.setWindowTitle(parent.windowTitle())
    return fd.getExistingDirectory(parent, text, de_dir)


def parseSemanticVersion(ver: str):
    return tuple([int(i) for i in ver.split(".")])


def getVersionString(ver: tuple):
    return ".".join([str(i) for i in ver])


def getInstallDir():
    return path.dirname(executable)


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


def noop(*args):
    return


def zip_dir(src, dst):
    zf = zipfile.ZipFile("{}.zip".format(dst), "w", zipfile.ZIP_DEFLATED)
    abs_src = os.path.abspath(src)
    for dirname, subdirs, files in os.walk(src):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            zf.write(absname, arcname)
    zf.close()
