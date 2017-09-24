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
        manual = True
        existing = [i for i in instance.mods if i.proj == modid]
        if len(existing) > 0:
            for i in existing:
                manual = i.manual
                instance.uninstall_mod(i.file.filename)
        instance.install_mod(modid, f, curse, manual, self.prog_1.emit)
        self.done.emit(1)
        self.exit()

    def download_pack(self, pack: CurseModpack, f: CurseFile):
        pack.install(f, self.label.emit, self.prog_1.emit, self.prog_2.emit)
        self.done.emit(1)
        self.exit()

    def download_file(self, f: str, path: str, curse: CurseAPI, fname=""):
        curse.download_file(f, path, fname)
        self.done.emit(1)
        self.exit()
