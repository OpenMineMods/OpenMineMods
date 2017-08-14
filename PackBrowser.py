from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from CurseAPI import CurseAPI, CurseProject, SearchType, CurseModpack
from functools import partial
from MultiMC import MultiMC
from Utils import clearLayout, msgBox
from threading import Thread


class PackBrowseWindow(QWidget):
    def __init__(self, curse: CurseAPI, mmc: MultiMC, parent: QWidget):
        super().__init__()

        self.curse = curse
        self.mmc = mmc
        self.parent = parent

        self.page = 0

        self.setWindowTitle("Browsing Modpacks")

        self.layout = QVBoxLayout(self)

        self.searchBox = QGroupBox("Search Modpacks")
        self.layout.addWidget(self.searchBox)

        self.searchGrid = QGridLayout()

        searchBut = QPushButton("Go")
        searchBut.clicked.connect(self.init_packs)
        self.searchGrid.addWidget(searchBut, 0, 1)

        self.searchInp = QLineEdit(self)
        self.searchInp.returnPressed.connect(searchBut.click)
        self.searchGrid.addWidget(self.searchInp, 0, 0)

        self.searchBox.setLayout(self.searchGrid)

        self.packBox = QGroupBox("Available Modpacks")
        self.layout.addWidget(self.packBox)

        self.packTable = QVBoxLayout()

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

        def create_pack_item(pack):
            group = QGroupBox(self)
            hbox = QHBoxLayout()
            group.setLayout(hbox)
            group.setStyleSheet("QGroupBox { border:0; } ")
            addButton = QPushButton("Install", self)
            addButton.clicked.connect(partial(self.add_clicked, pack=pack))
            hbox.addStretch(0)
            hbox.addWidget(addButton)
            hbox.addWidget(QLabel(pack.title))
            return group

        for pack in packs:
            self.packTable.addWidget(create_pack_item(pack),0, Qt.AlignLeft)

    def add_clicked(self, pack: CurseProject):
        msgBox(self, QMessageBox.Information, "Installing {} in background!".format(pack.title))
        project = CurseProject(self.curse.get(path="/projects/{}".format(pack.id), host=self.curse.forgeUrl),
                               detailed=True)
        pack = CurseModpack(project, self.curse, self.mmc)
        Thread(target=self.packdlThread, args=(pack,)).start()

    def packdlThread(self, pack: CurseModpack):
        file = self.curse.get_files(pack.project.id)[0]
        pack.install(file)
        self.mmc.metaDb.close()
        self.mmc = MultiMC(self.curse.baseDir)
        self.parent.init_instances()
        msgBox(icon=QMessageBox.Information, text="Finished installing {}!".format(pack.project.title))
