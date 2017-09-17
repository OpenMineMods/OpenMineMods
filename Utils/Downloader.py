from PyQt5.QtCore import QThread, pyqtSignal

from API.CurseAPI import CurseFile, CurseAPI
from API.MultiMC import MultiMCInstance


class DownloaderThread(QThread):
    label = pyqtSignal(str)
    prog_1 = pyqtSignal(int)
    prog_2 = pyqtSignal(int)

    done = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    def download_mod(self, modid: str, f: CurseFile, curse: CurseAPI, instance: MultiMCInstance):
        instance.install_mod(modid, f, curse, True, self.prog_1.emit)
        self.done.emit(1)
