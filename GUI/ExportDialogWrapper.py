from PyQt5.QtWidgets import *

from functools import partial
from os import path, listdir, makedirs, remove
from shutil import copytree, copy, rmtree
from getpass import getuser
from json import dumps

from API.MultiMC import MultiMCInstance
from API.CurseAPI import CurseAPI

from Utils.Utils import zip_dir

from GUI.ExportDialog import Ui_ExportDialog

from GUI.ExportWidget import Ui_ExportWidget


default_selected = [
    "config",
    "mods",
    "resources",
    "scripts"
]


class ExportDialog:
    def __init__(self, instance: MultiMCInstance, curse: CurseAPI, temp_dir: str):
        self.curse = curse
        self.instance = instance
        self.temp = path.join(temp_dir, instance.name)

        self.mc_dir = path.join(instance.path, "minecraft")

        self.dia = QDialog()
        self.ui = Ui_ExportDialog()
        self.ui.setupUi(self.dia)
        self.widgets = list()

        self.dia.setWindowTitle("Exporting {}".format(instance.name))

        for file in listdir(self.mc_dir):
            widget = QWidget()
            el = Ui_ExportWidget()
            el.setupUi(widget)

            el.label.setText(file)
            el.checkBox.setChecked(file in default_selected)

            self.widgets.append((el, file))
            self.ui.folder_layout.addWidget(widget)

        self.ui.folder_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.ui.export_button.clicked.connect(self.export_clicked)
        self.ui.cancel_button.clicked.connect(partial(self.dia.done, 0))

        self.dia.exec_()

    def export_clicked(self):
        to_export = list()
        for widget in self.widgets:
            if widget[0].checkBox.isChecked():
                to_export.append(widget[1])

        manifest = {
            "author": getuser(),
            "manifestType": "minecraftModpack",
            "manifestVersion": 1,
            "overrides": "overrides",
            "projectID": 1234567,
            "version": "1.0",
            "name": self.instance.name,
            "minecraft": {
                "modLoaders": [
                    {
                        "id": "forge-" + self.instance.forge,
                        "primary": True
                    }
                ],
                "version": self.instance.version
            },
            "files": list()
        }

        overrides_path = path.join(self.temp, "overrides")

        if path.exists(overrides_path):
            rmtree(overrides_path)

        makedirs(overrides_path)

        for f in to_export:
            if path.isfile(path.join(self.mc_dir, f)):
                copy(path.join(self.mc_dir, f), path.join(overrides_path, f))
            else:
                copytree(path.join(self.mc_dir, f), path.join(overrides_path, f))

        mods_path = path.join(overrides_path, "mods")
        if path.exists(mods_path):
            for mod in self.instance.mods:
                remove(path.join(mods_path, path.basename(mod["path"])))

        for mod in self.instance.mods:
            prj = self.curse.get_project(self.curse.get_file(mod["id"]).project).id
            manifest["files"].append({
                "fileID": mod["id"],
                "projectID": prj,
                "required": True
            })

        with open(path.join(self.temp, "manifest.json"), 'w+') as f:
            f.write(dumps(manifest, separators=(",", ":")))

        zip_dir(self.temp, path.join(path.expanduser("~"), self.instance.name))

        rmtree(self.temp)

        self.dia.done(1)
