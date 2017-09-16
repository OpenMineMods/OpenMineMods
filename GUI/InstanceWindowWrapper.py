from PyQt5.QtWidgets import *

from API.MultiMC import MultiMCInstance

from Utils.Utils import clear_layout

from GUI.InstanceWindow import Ui_InstanceWindow

from GUI.ModWidget import Ui_ModWidget


class InstanceWindow:
    def __init__(self, instance: MultiMCInstance):
        self.instance = instance

        self.win = QMainWindow()
        self.ui = Ui_InstanceWindow()

        self.ui.setupUi(self.win)

        self.win.setWindowTitle("Editing {}".format(instance.name))

        self.setup_mods()

        self.win.show()

    def setup_mods(self):
        clear_layout(self.ui.mod_box)
        for mod in self.instance.mods:
            widget = QWidget()
            el = Ui_ModWidget()
            el.setupUi(widget)

            el.mod_name.setText(mod.file.name)

            self.ui.mod_box.addWidget(widget)

        self.ui.mod_box.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
