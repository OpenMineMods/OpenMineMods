from PyQt5.QtWidgets import *
from CurseAPI import CurseAPI, CurseProject, SearchType
from functools import partial
from Utils import clearLayout


class PackBrowseWindow(QWidget):
    def __init__(self, curse: CurseAPI):
        super().__init__()

        self.curse = curse

        self.page = 0

        self.setWindowTitle("Browsing Modpacks")

        self.layout = QVBoxLayout()

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
        self.setLayout(self.layout)

        self.show()

    def init_packs(self):
        clearLayout(self.packTable)
        print("Cleared")
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
        print("Install {}".format(pack.title))
