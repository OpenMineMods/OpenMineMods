from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, QStandardPaths, QFile

import sys

from functools import partial
from os import path, makedirs
from webbrowser import open as webopen
from sys import platform
from json import loads
from time import time
from subprocess import Popen, DEVNULL
from glob import glob

from API.CurseAPI import CurseAPI, CurseProject
from API.MultiMC import MultiMC, MultiMCInstance

from CurseMetaDB.DB import DB

from Utils.Utils import clear_layout, confirm_box, dir_box, msg_box, get_multimc_executable, load_style_sheet, \
    human_format
from Utils.Updater import UpdateCheckThread, Update
from Utils.Logger import *
from Utils.Downloader import DownloaderThread
from Utils.Analytics import send_data
from Utils.Config import Config, Setting

from GUI.MainWindow import Ui_MainWindow

from GUI.InstanceWindowWrapper import InstanceWindow

from GUI.UpdateDialog import Ui_UpdateDialog

from GUI.FileDialogWrapper import FileDialog
from GUI.DownloadDialogWrapper import DownloadDialog
from GUI.InitialSetupWrapper import SetupWindow
from GUI.ExportDialogWrapper import ExportDialog

from GUI.InstanceWidget import Ui_InstanceWidget
from GUI.PackWidget import Ui_PackWidget

from GUI.FlowLayout import FlowLayout


class MainWindow:
    def __init__(self):
        data_dir = QStandardPaths.writableLocation(QStandardPaths.GenericConfigLocation)
        cache_dir = QStandardPaths.writableLocation(QStandardPaths.GenericCacheLocation)
        data_dir = path.join(data_dir, "openminemods")
        cache_dir = path.join(cache_dir, "openminemods")
        if not path.exists(data_dir):
            makedirs(data_dir)
        if not path.exists(cache_dir):
            makedirs(cache_dir)

        info("Data dir: {}".format(data_dir))
        info("Cache dir: {}".format(cache_dir))

        self.cache_dir = cache_dir
        self.icon_dir = path.join(self.cache_dir, "icons")

        if not path.isdir(self.icon_dir):
            makedirs(self.icon_dir)

        if not path.isfile(path.join(data_dir, "settings.ini")):
            dia = SetupWindow(data_dir, cache_dir)
            dia.win.exec_()

        self.conf = Config(data_dir)

        new_meta_time = self.conf.read(Setting.last_meta) + (self.conf.read(Setting.meta_interval) * 60 ** 3)

        if not path.isfile(path.join(cache_dir, "meta.json")) or int(time()) > new_meta_time:
            dia = SetupWindow(data_dir, cache_dir)
            dia.next_tab()
            dia.next_tab()
            dia.win.exec_()
            self.conf.write(Setting.last_meta, int(time()))

        self.db = DB(loads(open(path.join(cache_dir, "meta.json")).read()))

        self.curse = CurseAPI(self.db)

        if self.conf.read(Setting.analytics):
            if self.curse.version != self.conf.read(Setting.current_version):
                info("Sending analytics packet")
                send_data(self.conf)

        self.conf.write(Setting.current_version, self.curse.version)

        self.win = QMainWindow()

        self.style = load_style_sheet('main')

        self.win.setStyleSheet(self.style)

        self.mmc = MultiMC(self.conf.read(Setting.location))
        self.mmc_exe = get_multimc_executable(self.conf.read(Setting.location))

        self.children = list()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.win)

        self.ui.instance_box = FlowLayout()
        self.ui.scroll_box_w.setLayout(self.ui.instance_box)

        self.init_instances()

        self.ui.mmc_folder.setText(self.conf.read(Setting.location))

        self.ui.analytics_check.setChecked(self.conf.read(Setting.analytics))
        self.ui.analytics_check.clicked.connect(self.analytics_checked)

        self.ui.update_check.setChecked(self.conf.read(Setting.update))
        self.ui.update_check.clicked.connect(self.update_checked)

        self.ui.file_check.setChecked(self.conf.read(Setting.ask_file))
        self.ui.file_check.clicked.connect(self.file_checked)

        self.ui.search_check.setChecked(self.conf.read(Setting.live_search))
        self.ui.search_check.clicked.connect(self.search_checked)

        self.ui.pack_search.textChanged.connect(self.q_typed)
        self.ui.pack_search.returnPressed.connect(self.search_packs)
        self.ui.pack_search_button.clicked.connect(self.search_packs)

        self.ui.instance_reload.clicked.connect(self.init_instances)

        self.ui.mmc_edit.clicked.connect(self.dir_clicked)

        self.win.setWindowTitle("OpenMineMods v{}".format(self.curse.version))

        self.ui.ad_img = QWidget()
        self.ui.ad_img.setStyleSheet(".QWidget { border-image: url(:/icons/ad.png) }")
        self.ui.ad_img.setFixedSize(60, 40)
        self.ui.ad_img.setParent(self.win)

        self.win.resizeEvent = self.resizeEvent

        self.icon_threads = []
        self.init_packs(self.curse.get_modpacks())

        self.win.show()

        if self.conf.read(Setting.update) and getattr(sys, "frozen", False):
            new_client_time = self.conf.read(Setting.last_client) + (self.conf.read(Setting.client_interval) * 60 ** 3)
            if int(time()) > new_client_time:
                info("Starting update check")
                self.update_tr = QThread()
                self.uc = UpdateCheckThread(self.curse)
                self.uc.done.connect(self.update_check_done)

                self.uc.moveToThread(self.update_tr)
                self.update_tr.started.connect(self.uc.check_updates)

                self.update_tr.start()

    """UI Initializations"""

    def init_instances(self):
        self.mmc = MultiMC(self.conf.read(Setting.location))
        clear_layout(self.ui.instance_box)

        icons = path.join(self.mmc.path, "icons")

        for instance in self.mmc.instances:
            widget = QWidget()
            el = Ui_InstanceWidget()

            el.setupUi(widget)

            icon = glob(path.join(icons, instance.iconKey + ".*"))
            if len(icon) > 0:
                widget.setStyleSheet(".QWidget { border-image: url(" + icon[0] + "); }")
            else:
                widget.setStyleSheet(".QWidget { border-image: url(:/icons/OpenMineMods.svg); }")
            el.instance_delete.clicked.connect(partial(self.delete_clicked, instance))
            el.instance_edit.clicked.connect(partial(self.edit_clicked, instance))
            el.share_button.clicked.connect(partial(ExportDialog, instance, self.curse, self.cache_dir))

            el.instance_update.hide()

            if instance.file:
                f = self.curse.get_file(instance.file)
                p = self.curse.get_project(f.project)

                el.instance_update.clicked.connect(partial(self.install_clicked, p, True))

                fs = [self.curse.get_file(i) for i in p.files]
                fs.sort(key=lambda x: x.pub_time, reverse=True)

                if fs[0].pub_time > f.pub_time:
                    el.instance_update.show()

            el.instance_name.setText(instance.name)

            if self.mmc_exe:
                el.play_button.clicked.connect(
                    partial(Popen, [self.mmc_exe, '-l', path.basename(instance.path)], stdout=DEVNULL, stderr=DEVNULL))
            else:
                el.play_button.hide()

            self.ui.instance_box.addWidget(widget)

        self.ui.instance_box.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def init_packs(self, packs: list):
        clear_layout(self.ui.pack_box)

        for pack in packs:
            widget = QWidget()
            el = Ui_PackWidget()
            el.setupUi(widget)
            el.pack_downloads.setText("Downloads: {}".format(human_format(pack.downloads)))
            el.pack_authors.setText("By {}".format(', '.join(pack.authors)))
            el.pack_mcver.setText("Minecraft {}".format(pack.versions[-1]))
            el.pack_desc.setText(pack.desc)
            el.pack_name.setText(pack.name)
            el.pack_install.clicked.connect(partial(self.install_clicked, pack))
            el.pack_more.clicked.connect(partial(webopen, pack.page))

            if pack.icon_name is not None:
                icon = path.join(self.icon_dir, pack.icon_name)
                if not path.isfile(icon):
                    icon_thread = QThread()
                    dltr = DownloaderThread()
                    dltr.moveToThread(icon_thread)
                    icon_thread.started.connect(
                        partial(dltr.download_file_raw, pack.icon_url, self.icon_dir, pack.icon_name))
                    dltr.done.connect(partial(el.pack_icon.setStyleSheet,
                                              ".QWidget { border-image: url(" +
                                              path.join(self.icon_dir, pack.icon_name) + "); }"))
                    icon_thread.start()
                    self.icon_threads.append(icon_thread)
                else:
                    el.pack_icon.setStyleSheet(".QWidget { border-image: url(" + icon + "); }")
            else:
                icon = ":/icons/OpenMineMods.svg"
                el.pack_icon.setStyleSheet(".QWidget { border-image: url(" + icon + "); }")

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
        if not confirm_box(self.win, QMessageBox.Question,
                           "Are you sure you want to delete {}".format(instance.name)):
            return
        self.mmc.delete_instance(instance)
        self.init_instances()

    def edit_clicked(self, instance: MultiMCInstance):
        self.children.append(InstanceWindow(instance, self.curse, self.conf))

    def install_clicked(self, project: CurseProject, force_latest=False):
        fs = [self.curse.get_file(i) for i in project.files]
        if len(fs) < 1:
            return False
        fs.sort(key=lambda x: x.pub_time, reverse=True)
        if self.conf.read(Setting.ask_file) and not force_latest:
            dia = FileDialog(fs)
            f = dia.dia.exec_()
            if not f:
                return

            f = fs[f - 1]

        else:
            f = fs[0]

        dia = DownloadDialog()
        dia.download_pack(project, f, self.curse, self.mmc, force_latest)
        self.mmc = MultiMC(self.conf.read(Setting.location))
        self.init_instances()

    # Settings Checkboxes

    def analytics_checked(self):
        self.conf.write(Setting.analytics, self.ui.analytics_check.isChecked())

    def update_checked(self):
        self.conf.write(Setting.update, self.ui.update_check.isChecked())

    def file_checked(self):
        self.conf.write(Setting.ask_file, self.ui.file_check.isChecked())

    def search_checked(self):
        self.conf.write(Setting.live_search, self.ui.search_check.isChecked())

    def dir_clicked(self):
        ndir = dir_box(self.win, "MultiMC Folder", path.expanduser("~"))
        if ndir:
            self.conf.write(Setting.location, ndir)
            self.ui.mmc_folder.setText(ndir)
            msg_box(self.win, "A restart is required for settings to take effect")

    # Update Checker

    def update_check_done(self, res: dict):
        self.conf.write(Setting.last_client, int(time()))
        if not res["res"] or not res["update"]["downloads"][platform]:
            return

        up_win = QDialog()
        upd = Ui_UpdateDialog()
        upd.setupUi(up_win)

        upd.textBrowser.setText(res["update"]["changelog"])

        if not up_win.exec_():
            return

        update = Update(self.curse, res["update"])
        update.apply_update()

    def resizeEvent(self, event):
        self.ui.ad_img.move(self.win.width() - self.ui.ad_img.width() - 10, 10)
