import shutil

from PyQt5.QtCore import QThread, pyqtSignal
from requests import get
from os import path, makedirs, remove, listdir
from sys import platform, executable
from zipfile import ZipFile

from GUI.Strings import Strings

from API.CurseAPI import CurseAPI
from Utils.Utils import parseSemanticVersion, msg_box
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

        vers = get("https://openminemods.digitalfishfun.com/versions.json").json()
        latest = parseSemanticVersion(vers["v2_latest_stable"])

        if latest > ver:
            self.done.emit({
                "res": True,
                "update": vers["versions"][vers["v2_latest_stable"]],
                "ver": vers["v2_latest_stable"]
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

        self.idir = path.dirname(executable)

        if platform != "linux":
            self.ext = "." + dl_url.split(".")[-1]
        else:
            self.ext = ""

        self.dlwin = DownloadDialog()
        self.dlwin.download_file(dl_url, self.idir, self.curse, "OpenMineMods_Update" + self.ext)

        remove(executable)

        shutil.move(path.join(self.idir, "OpenMineMods_Update" + self.ext), executable)

        msg_box(None, text=translate("prompt.update.restart"))
