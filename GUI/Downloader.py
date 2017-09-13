from PyQt5.QtCore import QThread, pyqtSignal
from API.CurseAPI import CurseAPI, CurseFile, CurseModpack
from PyQt5.QtWidgets import *

from GUI.Strings import Strings

strings = Strings()
translate = strings.get


class FileDownloaderWindow(QWidget):
    def __init__(self, file: str, curse: CurseAPI, path: str, fname=False, callback=False):
        super().__init__()

        self.callback = callback

        self.setWindowTitle(translate("downloading.update"))

        self.layout = QVBoxLayout(self)

        self.progress = QProgressBar()
        self.layout.addWidget(self.progress)

        self.show()

        self.downloader = FileDownloaderThread(file, curse, path, fname)
        self.downloader.done.connect(self.download_done)
        self.downloader.update.connect(self.progress.setValue)

        self.download_thread = QThread()

        self.downloader.moveToThread(self.download_thread)

        self.download_thread.started.connect(self.downloader.download)
        self.download_thread.start()

    def download_done(self):
        if self.callback:
            self.callback()
        self.close()


class FileDownloaderThread(QThread):
    done = pyqtSignal()
    update = pyqtSignal(int, name="ping")

    def __init__(self, file: str, curse: CurseAPI, path: str, fname: str):
        super().__init__()

        self.file = file
        self.path = path
        self.fname = fname
        self.curse = curse

    def download(self):
        self.curse.download_file(self.file, self.path, self.fname, self.update.emit)

        self.done.emit()


class ModDownloaderWindow(QWidget):
    def __init__(self, file: CurseFile, curse: CurseAPI, instance, initmods):
        super().__init__()

        self.initmods = initmods

        self.setWindowTitle(translate("downloading.mod").format(file.name))

        self.layout = QVBoxLayout(self)

        self.progress = QProgressBar()
        self.layout.addWidget(self.progress)

        self.show()

        self.downloader = ModDownloaderThread(file, curse, instance)
        self.downloader.done.connect(self.download_done)
        self.downloader.update.connect(self.progress.setValue)

        self.download_thread = QThread()

        self.downloader.moveToThread(self.download_thread)

        self.download_thread.started.connect(self.downloader.download)
        self.download_thread.start()

    def download_done(self):
        self.initmods()
        self.close()


class ModDownloaderThread(QThread):
    done = pyqtSignal()
    update = pyqtSignal(int, name="ping")

    def __init__(self, file: CurseFile, curse: CurseAPI, instance):
        super().__init__()

        self.file = file
        self.curse = curse
        self.instance = instance

    def download(self):
        self.instance.install_mod(self.file, self.curse, True, self.update.emit)

        self.done.emit()


class PackDownloaderWindow(QWidget):
    def __init__(self, file: CurseFile, curse: CurseAPI, pack: CurseModpack):
        super().__init__()

        self.setWindowTitle(translate("downloading.pack").format(pack.project.title))

        self.layout = QVBoxLayout(self)

        self.label = QLabel()
        self.layout.addWidget(self.label)

        self.progress = QProgressBar()
        self.layout.addWidget(self.progress)

        self.prog2 = QProgressBar()
        self.layout.addWidget(self.prog2)

        self.show()

        self.downloader = PackDownloaderThread(file, curse, pack)
        self.downloader.done.connect(self.download_done)
        self.downloader.bar1.connect(self.progress.setValue)
        self.downloader.bar2.connect(self.prog2.setValue)
        self.downloader.setLabel.connect(self.label.setText)

        self.download_thread = QThread()

        self.downloader.moveToThread(self.download_thread)

        self.download_thread.started.connect(self.downloader.download)
        self.download_thread.start()

    def download_done(self):
        self.close()


class PackDownloaderThread(QThread):
    done = pyqtSignal()
    setLabel = pyqtSignal(str, name="label")
    bar1 = pyqtSignal(int, name="bar1")
    bar2 = pyqtSignal(int, name="bar2")

    def __init__(self, file: CurseFile, curse: CurseAPI, pack: CurseModpack):
        super().__init__()

        self.file = file
        self.curse = curse
        self.pack = pack

    def download(self):
        self.pack.install(self.file, self.setLabel.emit, self.bar1.emit, self.bar2.emit)

        self.done.emit()
