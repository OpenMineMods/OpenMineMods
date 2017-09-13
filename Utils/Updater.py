from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from requests import get

from API.CurseAPI import CurseAPI
from Utils.Utils import parseSemanticVersion


class UpdateCheckThread(QThread):
    done = pyqtSignal(dict, name="done")

    def __init__(self, curse: CurseAPI):
        super().__init__()

        self.curse = curse

    def check_updates(self):
        ver = parseSemanticVersion(self.curse.version)

        vers = get("https://openminemods.digitalfishfun.com/versions.json").json()
        latest = parseSemanticVersion(vers["latest_stable"])

        if latest > ver:
            self.done.emit({
                "res": True,
                "update": vers["versions"][vers["latest_stable"]],
                "ver": vers["latest_stable"]
            })
            return

        self.done.emit({"res": False})
