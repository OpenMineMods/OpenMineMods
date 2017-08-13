from PyQt5.QtWidgets import *

def clearLayout(layout):
    print(layout.count())
    for i in reversed(range(layout.count())):
        layout.itemAt(i).widget().setParent(None)
    for i in range(layout.count()):
        print(i)


def confirmBox(parent, icon, text):
    msgbox = QMessageBox(parent)
    msgbox.setIcon(icon)
    msgbox.setText(text)
    msgbox.addButton(QMessageBox.Yes)
    msgbox.addButton(QMessageBox.No)
    msgbox.setDefaultButton(QMessageBox.No)

    return msgbox.exec_() == QMessageBox.Yes