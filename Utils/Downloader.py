from PyQt5.QtCore import QThread, pyqtSignal

from API.CurseAPI import CurseFile, CurseAPI, CurseModpack
from API.MultiMC import MultiMC, MultiMCInstance


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
        self.exit(1)

    def download_pack(self, pack: CurseModpack, f: CurseFile):
        pack.install(f, self.label.emit, self.prog_1.emit, self.prog_2.emit)
        self.done.emit(1)
        self.exit(0)
