from PyQt5.QtWidgets import *
from CurseAPI import CurseAPI, CurseProject, SearchType, CurseModpack
from functools import partial
from MultiMC import MultiMC
from Utils import clearLayout, msgBox
from threading import Thread


class PackBrowseWindow(QWidget):
    def __init__(self, curse: CurseAPI, mmc: MultiMC):
        super().__init__()

        self.curse = curse
        self.mmc = mmc

        self.page = 0

        self.setWindowTitle("Browsing Modpacks")

        self.layout = QVBoxLayout(self)

        self.searchBox = QGroupBox("Search Modpacks")
        self.layout.addWidget(self.searchBox)

        self.searchGrid = QGridLayout()

        self.searchInp = QLineEdit(self)
        self.searchGrid.addWidget(self.searchInp, 0, 0)
        searchBut = QPushButton("Go")
        searchBut.clicked.connect(self.init_packs)
        self.searchGrid.addWidget(searchBut, 0, 1)

        self.searchBox.setLayout(self.searchGrid)

        self.packBox = QGroupBox("Available Modpacks")
        self.layout.addWidget(self.packBox)

        self.packTable = QGridLayout()

        self.init_packs()

        self.packBox.setLayout(self.packTable)

        scroll = QScrollArea()
        scroll.setWidget(self.packBox)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(400)
        self.layout.addWidget(scroll)

        self.show()

    def init_packs(self):
        clearLayout(self.packTable)
        if self.searchInp.text():
            packs = self.curse.search(self.searchInp.text(), SearchType.Modpack)
        else:
            packs = self.curse.get_modpacks(page=self.page)

        for x, pack in enumerate(packs):
            addButton = QPushButton("Install", self)
            addButton.clicked.connect(partial(self.add_clicked, pack=pack))
            self.packTable.addWidget(QLabel(pack.title), x, 0)
            self.packTable.addWidget(addButton, x, 1)

    def add_clicked(self, pack: CurseProject):
        project = CurseProject(self.curse.get(path="/projects/{}".format(pack.id), host=self.curse.forgeUrl),
                               detailed=True)
        pack = CurseModpack(project, self.curse, self.mmc)
        Thread(target=self.packdlThread, args=(pack,)).start()
        msgBox(self, QMessageBox.Information, "Installing {} in background!".format(project.title))

    def packdlThread(self, pack: CurseModpack):
        file = self.curse.get_files(pack.project.id)[0]
        pack.install(file)
        self.mmc.metaDb.close()
        self.mmc = MultiMC(self.curse.baseDir)
        msgBox(self, QMessageBox.Information, "Finished installing {}!".format(pack.project.title))
