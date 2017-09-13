from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from API.CurseAPI import CurseAPI, CurseProject
from API.MultiMC import MultiMCInstance
from functools import partial
from Utils.Utils import clearLayout, makeIconButton

from GUI.Strings import Strings

from GUI.Downloader import ModDownloaderWindow

strings = Strings()
translate = strings.get


class ModBrowseWindow(QWidget):
    def __init__(self, curse: CurseAPI, instance: MultiMCInstance, parent: QWidget):
        super().__init__()

        self.curse = curse
        self.instance = instance
        self.parent = parent
        self.dl_win = None

        self.page = 0

        self.setWindowTitle(translate("title.browsing.mod").format(instance.name))

        self.layout = QVBoxLayout(self)

        self.searchBox = QGroupBox(translate("label.search.mods"))
        self.layout.addWidget(self.searchBox)

        self.searchGrid = QGridLayout()

        searchBut = makeIconButton(self, "search", translate("tooltip.search"))
        searchBut.clicked.connect(self.init_mods)
        self.searchGrid.addWidget(searchBut, 0, 1)

        self.searchInp = QLineEdit(self)
        self.searchInp.returnPressed.connect(searchBut.click)
        self.searchGrid.addWidget(self.searchInp, 0, 0)

        self.searchBox.setLayout(self.searchGrid)

        self.modBox = QGroupBox(translate("label.available.mods"))
        self.layout.addWidget(self.modBox)

        self.modTable = QVBoxLayout()

        self.init_mods()

        self.modBox.setLayout(self.modTable)

        scroll = QScrollArea()
        scroll.setWidget(self.modBox)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(400)
        self.layout.addWidget(scroll)

        self.show()

    def init_mods(self):
        clearLayout(self.modTable)
        if self.searchInp.text():
            packs = self.curse.search(self.searchInp.text())
        else:
            packs = self.curse.get_mod_list(self.instance.version, page=self.page)

        def create_mod_item(mod):
            group = QGroupBox(self)
            hbox = QHBoxLayout()
            group.setLayout(hbox)
            group.setStyleSheet("QGroupBox { border:0; } ")

            addButton = makeIconButton(self, "download", translate("tooltip.install"))
            addButton.clicked.connect(partial(self.add_clicked, mod=mod))

            hbox.addStretch(1)
            hbox.addWidget(QLabel(mod.title))
            hbox.addWidget(addButton)
            return group

        for pack in packs:
            self.modTable.addWidget(create_mod_item(pack), 0, Qt.AlignRight)

    def add_clicked(self, mod: CurseProject):
        file = [i for i in self.curse.get_files(mod.id)][0]
        self.dl_win = ModDownloaderWindow(file, self.curse, self.instance, self.parent.init_mods)
