from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, QStandardPaths

from functools import partial
from os import path, makedirs
from webbrowser import open as webopen
from sys import platform
from json import loads

from API.CurseAPI import CurseAPI, CurseProject, CurseModpack
from API.MultiMC import MultiMC, MultiMCInstance

from CurseMetaDB.DB import DB

from Utils.Utils import clear_layout, confirm_box
from Utils.Updater import UpdateCheckThread
from Utils.Logger import *
from Utils.Config import Config, Setting

from GUI.MainWindow import Ui_MainWindow

from GUI.InstanceWindowWrapper import InstanceWindow

from GUI.UpdateDialog import Ui_UpdateDialog

from GUI.FileDialogWrapper import FileDialog
from GUI.DownloadDialogWrapper import DownloadDialog
from GUI.InitialSetupWrapper import SetupWindow

from GUI.InstanceWidget import Ui_InstanceWidget
from GUI.PackWidget import Ui_PackWidget


class MainWindow:
    def __init__(self):
        data_dir = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
        cache_dir = QStandardPaths.writableLocation(QStandardPaths.CacheLocation)
        if not path.exists(data_dir):
            makedirs(data_dir)
        if not path.exists(cache_dir):
            makedirs(cache_dir)

        info("Data dir: {}".format(data_dir))
        info("Cache dir: {}".format(cache_dir))

        if not path.isfile(path.join(data_dir, "settings.ini")):
            dia = SetupWindow(data_dir, cache_dir)
            dia.win.exec_()

        self.conf = Config(data_dir)
        self.db = DB(loads(open(path.join(cache_dir, "meta.json")).read()))
        self.curse = CurseAPI(self.db)

        self.conf.write(Setting.current_version, self.curse.version)

        self.win = QMainWindow()

        self.mmc = MultiMC(self.conf.read(Setting.location))

        self.children = list()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.win)

        self.init_instances()

        self.ui.mmc_folder.setText(self.conf.read(Setting.location))

        self.ui.analytics_check.setChecked(self.conf.read(Setting.analytics))
        self.ui.analytics_check.clicked.connect(self.analytics_checked)

        self.ui.update_check.setChecked(self.conf.read(Setting.update))
        self.ui.update_check.clicked.connect(self.update_checked)

        self.ui.file_check.setChecked(self.conf.read(Setting.ask_file))
        self.ui.file_check.clicked.connect(self.file_checked)

        self.ui.pack_search.textChanged.connect(self.q_typed)
        self.ui.pack_search.returnPressed.connect(self.search_packs)
        self.ui.pack_search_button.clicked.connect(self.search_packs)

        self.win.setWindowTitle("OpenMineMods v{}".format(self.curse.version))

        self.init_packs(self.curse.get_modpacks())

        self.win.show()

        if self.conf.read(Setting.update):
            self.update_tr = QThread()
            self.uc = UpdateCheckThread(self.curse)
            self.uc.done.connect(self.update_check_done)

            self.uc.moveToThread(self.update_tr)
            self.update_tr.started.connect(self.uc.check_updates)

            self.update_tr.start()

    """UI Initializations"""

    def init_instances(self):
        clear_layout(self.ui.instance_box)

        for instance in self.mmc.instances:
            widget = QWidget()
            el = Ui_InstanceWidget()

            el.setupUi(widget)

            el.instance_delete.clicked.connect(partial(self.delete_clicked, instance))
            el.instance_edit.clicked.connect(partial(self.edit_clicked, instance))

            el.instance_update.hide()

            el.instance_name.setText(instance.name)

            self.ui.instance_box.addWidget(widget)

        self.ui.instance_box.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def init_packs(self, packs: list):
        clear_layout(self.ui.pack_box)

        for pack in packs:
            widget = QWidget()
            el = Ui_PackWidget()

            el.setupUi(widget)

            el.pack_name.setText("{} (MC {})".format(pack.name, pack.versions[-1]))
            el.pack_install.clicked.connect(partial(self.install_clicked, pack))
            el.pack_more.clicked.connect(partial(webopen, pack.page))
            self.ui.pack_box.addWidget(widget)

        self.ui.pack_box.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def reset_packs(self):
        clear_layout(self.ui.pack_box)

        self.ui.pack_box.addWidget(self.ui.loading_label)
        self.ui.pack_box.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    """Event Listeners"""

    def q_typed(self):
        if not self.conf.read(Setting.live_search):
            return
        if self.ui.pack_search.text() == "":
            self.init_packs(self.curse.get_modpacks())
            return
        self.init_packs(self.curse.search(self.ui.pack_search.text(), "modpack"))

    def search_packs(self):
        if self.ui.pack_search.text() == "":
            self.init_packs(self.curse.get_modpacks())
            return
        self.init_packs(self.curse.search(self.ui.pack_search.text(), "modpack"))

    def delete_clicked(self, instance: MultiMCInstance):
        print(confirm_box(self.win, QMessageBox.Question,
                          "Are you sure you want to delete {}".format(instance.name)))
        self.mmc.delete_instance(instance)
        self.init_instances()

    def edit_clicked(self, instance: MultiMCInstance):
        self.children.append(InstanceWindow(instance, self.curse, self.conf))

    def install_clicked(self, project: CurseProject):
        fs = project.files
        if self.conf.read(Setting.ask_file):
            dia = FileDialog(fs)
            f = dia.dia.exec_()
            if not f:
                return

            f = fs[f - 1]

        else:
            f = fs[0]

        dia = DownloadDialog()
        dia.download_pack(project, self.curse.get_file(f), self.curse, self.mmc)
        self.mmc = MultiMC(self.conf.read(Setting.location))
        self.init_instances()

    # Settings Checkboxes

    def analytics_checked(self):
        self.conf.write(Setting.analytics, self.ui.analytics_check.isChecked())

    def update_checked(self):
        self.conf.write(Setting.update, self.ui.update_check.isChecked())

    def file_checked(self):
        self.conf.write(Setting.ask_file, self.ui.file_check.isChecked())

    # Update Checker

    def update_check_done(self, res: dict):
        if not res["res"] or not res["update"]["downloads"][platform]:
            return

        up_win = QDialog()
        upd = Ui_UpdateDialog()
        upd.setupUi(up_win)

        upd.textBrowser.setText(res["update"]["changelog"])

        if not up_win.exec_():
            return

    def data_found(self, dat: dict):
        if len(dat["res"]) < 1 and dat["succ"]:
            return

        if dat["type"] == "packs":
            if not dat["succ"]:
                err("Pack loading failed!")
                self.ui.loading_label.setText("Network Error!")
                return
            self.init_packs(dat["res"])
