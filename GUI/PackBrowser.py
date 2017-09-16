from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from API.CurseAPI import CurseAPI, CurseProject, SearchType, CurseModpack
from functools import partial
from API.MultiMC import MultiMC
from Utils.Utils import clearLayout, makeIconButton

from GUI.Strings import Strings

from GUI.Downloader import PackDownloaderWindow

strings = Strings()
translate = strings.get


class PackBrowseWindow(QWidget):
    def __init__(self, curse: CurseAPI, mmc: MultiMC):
        super().__init__()

        self.curse = curse
        self.mmc = mmc
        self.dlwin = list()

        self.page = 0

        self.setWindowTitle(translate("title.browsing.packs"))

        self.layout = QVBoxLayout(self)

        self.searchBox = QGroupBox(translate("label.search.packs"))
        self.layout.addWidget(self.searchBox)

        self.searchGrid = QGridLayout()

        searchBut = makeIconButton(self, "search", translate("tooltip.search"))
        searchBut.clicked.connect(self.init_packs)
        self.searchGrid.addWidget(searchBut, 0, 1)

        self.searchInp = QLineEdit(self)
        self.searchInp.returnPressed.connect(searchBut.click)
        self.searchGrid.addWidget(self.searchInp, 0, 0)

        self.searchBox.setLayout(self.searchGrid)

        self.packBox = QGroupBox(translate("label.available.packs"))
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

            addButton = makeIconButton(self, "download", translate("tooltip.install"))
            addButton.clicked.connect(partial(self.add_clicked, pack=pack))

            hbox.addStretch(1)
            hbox.addWidget(QLabel(pack.title))
            hbox.addWidget(addButton)
            return group

        for pack in packs:
            self.packTable.addWidget(create_pack_item(pack), 0, Qt.AlignRight)

    def add_clicked(self, pack: CurseProject):
        project = CurseProject(self.curse.get(path="/projects/{}".format(pack.id), host=self.curse.forgeUrl),
                               detailed=True)
        pack = CurseModpack(project, self.curse, self.mmc)
        file = self.curse.get_files(pack.project.id)[0]
        self.dlwin.append(PackDownloaderWindow(file, self.curse, pack))
