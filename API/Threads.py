from PyQt5.QtCore import QThread, pyqtSignal

from API.CurseAPI import CurseAPI, CurseProject


class CurseMetaThread(QThread):
    data_found = pyqtSignal(CurseProject)

    def __init__(self, curse: CurseAPI):
        super().__init__()

        self.curse = curse

    def get_packs(self, ver="", page=""):
        try:
            self.curse.get_modpacks(ver, page, callback=self.data_found.emit)
        except:
            return

    def get_mods(self, ver="", page=""):
        self.curse.get_mod_list(ver, page, callback=self.data_found.emit)

    def search(self, query: str, stype: str):
        try:
            self.curse.search(query, stype, callback=self.data_found.emit)
        except:
            return
