from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread

from functools import partial

from API.CurseAPI import CurseFile, CurseAPI, CurseProject, CurseModpack
from API.MultiMC import MultiMCInstance, MultiMC

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

    def download_mod(self, f: CurseFile, curse: CurseAPI, instance: MultiMCInstance):
        self.dia.setWindowTitle("Downloading {}".format(f.filename))
        self.ui.progbar_1.setValue(0)
        self.ui.status_label.hide()
        self.ui.progbar_2.hide()

        self.dlthread.started.connect(partial(self.downloader.download_mod, f, curse, instance))
        self.dlthread.start()
        return self.dia.exec_()

    def download_pack(self, project: CurseProject, file: CurseFile, curse: CurseAPI, mmc: MultiMC):
        self.dia.setWindowTitle("Downloading {}".format(project.name))
        self.ui.progbar_1.setValue(0)
        self.ui.progbar_2.setValue(0)

        pack = CurseModpack(project, curse, mmc)
        self.dlthread.started.connect(partial(self.downloader.download_pack, pack, file))
        self.dlthread.start()
        return self.dia.exec_()

    def download_file(self, f: str, path: str, curse: CurseAPI, fname: ""):
        if not fname:
            self.dia.setWindowTitle("Downloading {}".format(f.split("/")[-1]))
        else:
            self.dia.setWindowTitle("Downloading {}".format(fname))

        self.ui.progbar_1.setValue(0)
        self.ui.status_label.hide()
        self.ui.progbar_2.hide()

        self.dlthread.started.connect(partial(self.downloader.download_file, f, path, curse, fname))
        self.dlthread.start()
        return self.dia.exec_()

    def _dl_done(self, status: int):
        self.dlthread.exit()
        self.downloader.exit()
        self.dia.done(status)
