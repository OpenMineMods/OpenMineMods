import os
import zipfile

from os import path
from re import finditer
from sys import executable, platform

from PyQt5.QtCore import QFile
from PyQt5.QtWidgets import *


def confirmation(win, func, name):
    if not confirm_box(win, QMessageBox.Question,
                       "Are you sure you want to delete {}".format(name)):
        return
    func()


def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])


def load_style_sheet(sheet_name):
    vars = dict()
    file = QFile(':/style/%s.qss' % sheet_name.lower())
    file.open(QFile.ReadOnly)
    style_sheet = str(file.readAll(), encoding='utf8')
    for match in finditer("(\$.+):\s*(.+);", style_sheet):
        style_sheet = style_sheet.replace(match.group(0), "")
        vars[match.group(1)] = match.group(2)
    for name, val in vars.items():
        style_sheet = style_sheet.replace(name, val)
    for match in finditer("\$alpha\((.*),\s*(\d+)\)", style_sheet):
        color_code = match.group(1)[1:]
        rgba = (int(color_code[:2], 16), int(color_code[2:4], 16), int(color_code[4:], 16))
        alpha = int(match.group(2))
        new = "rgba({}, {}, {}, {})".format(rgba[0], rgba[1], rgba[2], alpha)
        style_sheet = style_sheet.replace(match.group(0), new)
    return style_sheet


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


def get_multimc_executable(mmc_dir: str):
    if platform == "linux":
        if path.isfile("/usr/bin/multimc"):
            return "/usr/bin/multimc"
        elif path.isfile(path.join(mmc_dir, "MultiMC")):
            return path.join(mmc_dir, "MultiMC")
        return False
    elif platform == "darwin":
        if path.isfile(path.join(mmc_dir, "MultiMC")):
            return path.join(mmc_dir, "MultiMC")
        return False
    elif platform == "win32":
        if path.isfile(path.join(mmc_dir, "MultiMC.exe")):
            return path.join(mmc_dir, "MultiMC.exe")
    return False


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
