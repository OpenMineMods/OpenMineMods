import sys
from PyQt5.QtWidgets import *
from MainWindow import Ui_MainWindow
from InstanceWidget import Ui_instance_obj

app = QApplication(sys.argv)
wg = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(wg)

for nm in ["Hello", "World"]:
    qw = QWidget()
    ie = Ui_instance_obj()
    ie.setupUi(qw)
    ie.instance_name.setText(nm)
    ui.instance_box.addWidget(qw)

ui.instance_box.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

wg.show()
sys.exit(app.exec_())
