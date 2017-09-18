from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread

from functools import partial

from API.CurseAPI import CurseFile, CurseAPI
from API.MultiMC import MultiMCInstance

from Utils.Downloader import DownloaderThread

from GUI.ProgressDialog import Ui_ProgressDialog


class DownloadDialog:
    def __init__(self):
        self.dia = QDialog()
        self.ui = Ui_ProgressDialog()
        self.ui.setupUi(self.dia)

        self.dlthread = QThread()
        self.downloader = DownloaderThread()

        self.downloader.moveToThread(self.dlthread)

        self.downloader.label.connect(self.ui.status_label.setText)
        self.downloader.prog_1.connect(self.ui.progbar_1.setValue)
        self.downloader.prog_2.connect(self.ui.progbar_2.setValue)

        self.downloader.done.connect(self._dl_done)

    def download_mod(self, modid: str, f: CurseFile, curse: CurseAPI, instance: MultiMCInstance):
        self.dia.setWindowTitle("Downloading {}".format(f.name))
        self.ui.progbar_1.setValue(0)
        self.ui.status_label.hide()
        self.ui.progbar_2.hide()

        self.dlthread.started.connect(partial(self.downloader.download_mod, modid, f, curse, instance))
        self.dlthread.start()
        self.dia.exec_()

    def _dl_done(self, status: int):
        try:
            self.dlthread.terminate()
        except:
            pass
        self.dia.done(status)
