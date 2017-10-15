from PyQt5.QtCore import QThread, pyqtSignal

from requests import get
from pathlib import Path
from urllib.parse import unquote

from API.CurseAPI import CurseFile, CurseAPI, CurseModpack
from API.MultiMC import MultiMCInstance


class DownloaderThread(QThread):
    label = pyqtSignal(str)
    prog_1 = pyqtSignal(int)
    prog_2 = pyqtSignal(int)

    done = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    def download_mod(self, f: CurseFile, curse: CurseAPI, instance: MultiMCInstance):
        existing = [i for i in instance.mods if curse.get_file(i["id"]).project == curse.get_file(f.id).project]
        if len(existing) > 0:
            for i in existing:
                instance.uninstall_mod(i["path"])
        instance.install_mod(f, curse, self.prog_1.emit)
        self.done.emit(1)

    def download_pack(self, pack: CurseModpack, f: CurseFile, u: bool):
        pack.install(f, self.label.emit, self.prog_1.emit, self.prog_2.emit, u)
        self.done.emit(1)

    def download_file(self, f: str, path: str, curse: CurseAPI, fname=""):
        curse.download_file(f, path, fname)
        self.done.emit(1)

    def download_file_raw(self, f: str, path: str, fname=""):
        r = get(f, stream=True)
        dlen = r.headers.get("content-length")
        try:
            step = (100 / int(dlen))
        except TypeError:
            step = 0
        prog = 0
        if not fname:
            fname = unquote(Path(r.url).name)
        with open(path+"/"+fname, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    prog += len(chunk)
                    self.prog_1.emit(int(step * prog))
                    f.write(chunk)
        self.done.emit(1)
