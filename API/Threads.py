from PyQt5.QtCore import QThread, pyqtSignal

from API.CurseAPI import CurseAPI


class CurseMetaThread(QThread):
    data_found = pyqtSignal(dict)

    def __init__(self, curse: CurseAPI):
        super().__init__()

        self.curse = curse

    def get_packs(self, ver="", page=""):
        try:
            packs = self.curse.get_modpacks(ver, page)
        except:
            self.data_found.emit({"type": "packs", "res": list(), "succ": False})
            return

        self.data_found.emit({"type": "packs", "res": packs, "succ": True})

    def get_mods(self, ver="", page=""):
        try:
            mods = self.curse.get_mod_list(ver, page)
        except:
            self.data_found.emit({"type": "mods", "res": list(), "succ": False})
            return

        self.data_found.emit({"type": "mods", "res": mods, "succ": True})

    def search(self, query: str, stype: str):
        try:
            res = self.curse.search(query, stype)
        except:
            self.data_found.emit({"type": stype, "res": list(), "succ": False})

        self.data_found.emit({"type": stype, "res": res, "succ": False})
