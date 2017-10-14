import shutil

from PyQt5.QtCore import QThread, pyqtSignal
from requests import get
from os import path, remove
from sys import platform, executable
from zipfile import ZipFile

from GUI.Strings import Strings

from API.CurseAPI import CurseAPI
from Utils.Utils import parseSemanticVersion, msg_box

from GUI.DownloadDialogWrapper import DownloadDialog


strings = Strings()
translate = strings.get

dl_data = {
    "linux": "Linux.zip",
    "darwin": "MacOS.zip",
    "win32": "Windows.zip"
}


class UpdateCheckThread(QThread):
    done = pyqtSignal(dict, name="done")

    def __init__(self, curse: CurseAPI):
        super().__init__()

        self.curse = curse

    def check_updates(self):
        ver = parseSemanticVersion(self.curse.version)

        vers = get("https://api.github.com/repos/OpenMineMods/OpenMineMods/releases").json()

        latest_ver = ver
        latest_release = False

        for release in vers:
            try:
                rel_ver = parseSemanticVersion(release["tag_name"][1:])
            except:
                continue
            if rel_ver > latest_ver:
                latest_release = release
                latest_ver = rel_ver

        if latest_release:
            out = {
                "url": latest_release["html_url"],
                "downloads": dict(),
                "changelog": latest_release["body"]
            }
            for dl in latest_release["assets"]:
                for nm in dl_data:
                    if dl_data[nm] == dl["name"]:
                        out["downloads"][nm] = dl["browser_download_url"]
            self.done.emit({
                "res": True,
                "update": out,
                "ver": latest_ver
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

        self.dlwin = DownloadDialog()
        self.dlwin.download_file(dl_url, self.idir, self.curse, "OpenMineMods_Update.zip")

        zipf = ZipFile("OpenMineMods_Update.zip")
        zipf.extractall("OpenMineMods_Update")

        remove("OpenMineMods_Update.zip")

        app_dir = path.dirname(path.dirname(path.dirname(executable)))
        if platform == "darwin" and path.basename(app_dir) == "OpenMineMods.app":
            shutil.rmtree(app_dir)
            shutil.move("OpenMineMods_Update", app_dir)
        else:
            remove(executable)
            shutil.move("OpenMineMods_Update", executable)

        msg_box(None, text=translate("prompt.update.restart"))
