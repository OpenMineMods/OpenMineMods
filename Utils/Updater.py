import shutil

from PyQt5.QtCore import QThread, pyqtSignal
from requests import get
from os import path, makedirs, remove, listdir
from sys import platform
from zipfile import ZipFile

from GUI.Strings import Strings

from API.CurseAPI import CurseAPI
from Utils.Utils import parseSemanticVersion, getInstallDir, msg_box
from Utils.Logger import err

from GUI.DownloadDialogWrapper import DownloadDialog


strings = Strings()
translate = strings.get


class UpdateCheckThread(QThread):
    done = pyqtSignal(dict, name="done")

    def __init__(self, curse: CurseAPI):
        super().__init__()

        self.curse = curse

    def check_updates(self):
        ver = parseSemanticVersion(self.curse.version)

        try:
            vers = get("https://openminemods.digitalfishfun.com/versions.json").json()
        except:
            err("Update check failed!")
            return
        latest = parseSemanticVersion(vers["latest_stable"])

        if latest > ver:
            self.done.emit({
                "res": True,
                "update": vers["versions"][vers["latest_stable"]],
                "ver": vers["latest_stable"]
            })
            return

        self.done.emit({"res": False})


class Update:
    def __init__(self, curse: CurseAPI, update: dict):
        self.curse = curse
        self.update = update
        self.dlwin = None
        self.idir = None

    def apply_update(self):
        dl_url = self.update["downloads"][platform]
        idir = getInstallDir()

        self.idir = idir

        self.dlwin = DownloadDialog()
        self.dlwin.download_file(dl_url, path.dirname(idir), self.curse, "omm-update.zip")
        self.zip_downloaded()

    def zip_downloaded(self):
        idir = self.idir
        odir = path.dirname(idir)

        makedirs(idir + ".new")

        f = ZipFile(odir + "/omm-update.zip")
        f.extractall(idir + ".new")
        f.close()

        remove(odir + "/omm-update.zip")

        shutil.move(idir, idir + ".old")
        shutil.move(idir + ".new/" + listdir(idir + ".new/")[0], idir)
        shutil.rmtree(idir + ".new")

        msg_box(text=translate("prompt.update.restart"))
