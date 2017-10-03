from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread

from os import path, remove
from functools import partial
from lzma import open as copen
from time import time

from Utils.Config import Config, Setting
from Utils.Utils import dir_box
from Utils.Downloader import DownloaderThread

from GUI.SetupDialog import Ui_SetupDialog


class SetupWindow:
    def __init__(self, config_folder: str, cache_folder: str):
        self.conf = Config(config_folder)
        self.cache = cache_folder
        self.win = QDialog()
        self.ui = Ui_SetupDialog()
        self.ui.setupUi(self.win)

        self.mmc_folder = ""

        self.ui.tabWidget.setTabEnabled(2, False)
        self.ui.pushButton.clicked.connect(self.next_tab)
        self.ui.pushButton_2.clicked.connect(self.next_tab)

        self.ui.mmc_folder.textChanged.connect(self.folder_changed)
        self.ui.toolButton.clicked.connect(self.file_search)

        self.dlthread = QThread()
        self.downloader = DownloaderThread()

        self.downloader.moveToThread(self.dlthread)

        self.downloader.label.connect(self.ui.prog_label.setText)
        self.downloader.prog_1.connect(self.ui.prog_1.setValue)

        self.downloader.done.connect(self._dl_done)

    def next_tab(self):
        ind = self.ui.tabWidget.currentIndex()
        if ind == 1:
            self.start_downloads()
            self.ui.tabWidget.setTabEnabled(0, False)
            self.ui.tabWidget.setTabEnabled(1, False)
        self.ui.tabWidget.setTabEnabled(ind + 1, True)
        self.ui.tabWidget.setCurrentIndex(ind + 1)

    def folder_changed(self):
        mmc_folder = self.ui.mmc_folder.text()
        self.mmc_folder = path.expanduser(mmc_folder)
        if path.isfile(path.join(self.mmc_folder, "multimc.cfg")):
            self.ui.pushButton_2.setEnabled(True)
        else:
            self.ui.pushButton_2.setEnabled(False)

    def start_downloads(self):
        if self.mmc_folder:
            self.conf.write(Setting.analytics, self.ui.analytics.isChecked())
            self.conf.write(Setting.update, self.ui.autoupdate.isChecked())

            self.conf.write(Setting.location, self.mmc_folder)

        self.ui.prog_label.setText("Downloading Latest CurseMeta")
        self.ui.prog_1.setValue(0)
        self.dlthread.started.connect(partial(self.downloader.download_file_raw,
                                              "https://openminemods.digitalfishfun.com/raw_cleaned.json.xz",
                                              self.cache))
        self.dlthread.start()

    def file_search(self):
        dir = dir_box(self.win, "Select your MultiMC folder", path.expanduser("~"))
        if dir:
            self.ui.mmc_folder.setText(dir)

    def _dl_done(self):
        self.ui.prog_label.setText("Decompressing CurseMeta")
        with copen(path.join(self.cache, "raw_cleaned.json.xz")) as f:
            with open(path.join(self.cache, "meta.json"), "wb+") as f2:
                f2.write(f.read())
        remove(path.join(self.cache, "raw_cleaned.json.xz"))
        self.conf.write(Setting.last_meta, int(time()))
        self.dlthread.terminate()
        self.downloader.terminate()
        self.win.done(1)
