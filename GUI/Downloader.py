from PyQt5.QtCore import QThread, pyqtSignal
from API.CurseAPI import CurseAPI, CurseFile
from PyQt5.QtWidgets import *


class ModDownloaderWindow(QWidget):
    def __init__(self, file: CurseFile, curse: CurseAPI, instance, initmods):
        super().__init__()

        self.initmods = initmods

        self.setWindowTitle("Downloading {}...".format(file.name))

        self.layout = QVBoxLayout(self)

        self.progress = QProgressBar()
        self.layout.addWidget(self.progress)

        self.show()

        self.downloader = DownloaderThread(file, curse, instance)
        self.downloader.done.connect(self.download_done)
        self.downloader.update.connect(self.progress.setValue)

        self.download_thread = QThread()

        self.downloader.moveToThread(self.download_thread)

        self.download_thread.started.connect(self.downloader.download)
        self.download_thread.start()

    def download_done(self):
        self.initmods()
        self.close()


class DownloaderThread(QThread):
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
