from PyQt5.QtWidgets import *

from functools import partial
from webbrowser import open as webopen

from API.MultiMC import MultiMCInstance
from API.CurseAPI import CurseAPI, CurseProject

from Utils.Utils import clear_layout

from GUI.InstanceWindow import Ui_InstanceWindow

from GUI.FileDialogWrapper import FileDialog
from GUI.DownloadDialogWrapper import DownloadDialog

from GUI.ModWidget import Ui_ModWidget


class InstanceWindow:
    def __init__(self, instance: MultiMCInstance, curse: CurseAPI):
        self.curse = curse
        self.instance = instance

        self.mod_widgets = list()

        self.win = QMainWindow()
        self.ui = Ui_InstanceWindow()

        self.ui.setupUi(self.win)

        self.win.setWindowTitle("Editing {}".format(instance.name))

        self.ui.pack_version.setText("Minecraft: {}".format(instance.version))

        if instance.file is not None:
            self.file = self.curse.get_file(instance.file)
            self.pack = self.curse.get_project(self.file.project)
            self.ui.pack_pack.setText("Modpack ID: {} ({})".format(self.pack.name, self.file.pub_time))
        else:
            self.file = None
            self.pack = None
            self.ui.pack_pack.hide()

        self.setup_mods()

        self.win.show()

    def clear_browse(self):
        for m in self.mod_widgets:
            m.setParent(None)

        self.mod_widgets = list()

    def setup_mods(self):
        clear_layout(self.ui.mod_box)
        for mod in self.instance.mods:
            widget = QWidget()
            el = Ui_ModWidget()
            el.setupUi(widget)

            modf = self.curse.get_file(mod["id"])
            proj = self.curse.get_project(modf.project)
            el.mod_name.setText(proj.name)

            el.mod_install.hide()
            el.mod_info.hide()
            el.mod_update.hide()

            self.ui.mod_box.addWidget(widget)

        self.ui.mod_box.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def mod_install(self, mod: CurseProject):
        fs = [i for i in mod.files if i.mc_ver == self.instance.version][::-1]
        if self.curse.db["filepick"]:
            dia = FileDialog(fs)
            f = dia.dia.exec_()
            if not f:
                return

            f = fs[f - 1]

        else:
            f = fs[0]

        dia = DownloadDialog()
        print(dia.download_mod(mod.id, f, self.curse, self.instance))
        self.setup_mods()
