from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread

from functools import partial
from webbrowser import open as webopen

from API.MultiMC import MultiMCInstance
from API.CurseAPI import CurseAPI
from API.Threads import CurseMetaThread

from Utils.Utils import clear_layout
from Utils.Logger import *

from GUI.InstanceWindow import Ui_InstanceWindow

from GUI.ModWidget import Ui_ModWidget


class InstanceWindow:
    def __init__(self, instance: MultiMCInstance, curse: CurseAPI):
        self.curse = curse
        self.instance = instance

        self.curse_mthread = CurseMetaThread(self.curse)
        self.curse_thread = QThread()

        self.curse_mthread.moveToThread(self.curse_thread)
        self.curse_mthread.data_found.connect(self.data_found)

        self.win = QMainWindow()
        self.ui = Ui_InstanceWindow()

        self.ui.setupUi(self.win)

        self.win.setWindowTitle("Editing {}".format(instance.name))

        self.ui.pack_version.setText("Minecraft: {}".format(instance.version))

        if instance.pack is not None:
            self.ui.pack_pack.setText("Modpack: {}".format(instance.pack.title))
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

    def setup_mod_browse(self, mods: list()):
        clear_layout(self.ui.browse_box)
        for mod in mods:
            widget = QWidget()
            el = Ui_ModWidget()
            el.setupUi(widget)

            el.mod_name.setText(mod.title)
            el.mod_info.clicked.connect(partial(webopen, mod.page))

            el.mod_delete.hide()
            el.mod_update.hide()

            self.ui.browse_box.addWidget(widget)

        self.ui.browse_box.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def data_found(self, dat: dict):
        if len(dat["res"]) < 1 and dat["succ"]:
            return

        if dat["type"] == "mods":
            if not dat["succ"]:
                self.ui.loading_label.setText("Network Error!")
                err("Mod loading failed!")
                return
            self.setup_mod_browse(dat["res"])
