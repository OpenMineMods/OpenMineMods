from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread

from functools import partial
from webbrowser import open as webopen

from API.MultiMC import MultiMCInstance
from API.CurseAPI import CurseAPI, CurseProject
from API.Threads import CurseMetaThread

from Utils.Utils import clear_layout

from GUI.InstanceWindow import Ui_InstanceWindow

from GUI.FileDialogWrapper import FileDialog
from GUI.DownloadDialogWrapper import DownloadDialog

from GUI.ModWidget import Ui_ModWidget


class InstanceWindow:
    def __init__(self, instance: MultiMCInstance, curse: CurseAPI):
        self.curse = curse
        self.instance = instance

        self.curse_mthread = CurseMetaThread(self.curse)
        self.curse_thread = QThread()

        self.curse_mthread.moveToThread(self.curse_thread)
        self.curse_mthread.data_found.connect(self.mod_found)

        self.win = QMainWindow()
        self.ui = Ui_InstanceWindow()

        self.ui.setupUi(self.win)

        self.win.setWindowTitle("Editing {}".format(instance.name))

        self.ui.pack_version.setText("Minecraft: {}".format(instance.version))

        if instance.pack is not None:
            self.ui.pack_pack.setText("Modpack ID: {}".format(instance.pack))
        else:
            self.ui.pack_pack.hide()

        self.setup_mods()

        self.win.show()

        self.curse_thread.started.connect(partial(self.curse_mthread.get_mods, instance.version))
        self.curse_thread.start()

    def setup_mods(self):
        clear_layout(self.ui.mod_box)
        for mod in self.instance.mods:
            widget = QWidget()
            el = Ui_ModWidget()
            el.setupUi(widget)

            el.mod_name.setText(mod.file.name)

            el.mod_install.hide()
            el.mod_info.hide()
            el.mod_update.hide()

            self.ui.mod_box.addWidget(widget)

        self.ui.mod_box.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def mod_found(self, mod: CurseProject):
        widget = QWidget()
        el = Ui_ModWidget()

        el.setupUi(widget)

        el.mod_name.setText(mod.name)
        el.mod_install.clicked.connect(partial(self.mod_install, mod))
        el.mod_info.clicked.connect(partial(webopen, mod.page))

        el.mod_delete.hide()
        el.mod_update.hide()

        self.ui.browse_box.insertWidget(self.ui.browse_box.count() - 2, widget)

    def mod_install(self, mod: CurseProject):
        fs = [i for i in mod.files if i.mc_ver == self.instance.version][::-1]
        if self.curse.db["filepick"]:
            dia = FileDialog(fs)
            f = dia.dia.exec_()
            if not f:
                return

            f = fs[f - 1]

        else:
            f = fs[-1]

        dia = DownloadDialog()
        dia.download_mod(mod.id, f, self.curse, self.instance)
