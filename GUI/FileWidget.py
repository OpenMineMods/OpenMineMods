# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/FileWidget.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FileWidget(object):
    def setupUi(self, FileWidget):
        FileWidget.setObjectName("FileWidget")
        FileWidget.resize(400, 41)
        FileWidget.setMaximumSize(QtCore.QSize(16777215, 41))
        self.verticalLayout = QtWidgets.QVBoxLayout(FileWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.file_name = QtWidgets.QLabel(FileWidget)
        self.file_name.setObjectName("file_name")
        self.horizontalLayout.addWidget(self.file_name)
        self.install_button = QtWidgets.QToolButton(FileWidget)
        icon = QtGui.QIcon.fromTheme("down")
        self.install_button.setIcon(icon)
        self.install_button.setObjectName("install_button")
        self.horizontalLayout.addWidget(self.install_button)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(FileWidget)
        QtCore.QMetaObject.connectSlotsByName(FileWidget)

    def retranslateUi(self, FileWidget):
        _translate = QtCore.QCoreApplication.translate
        FileWidget.setWindowTitle(_translate("FileWidget", "Form"))
        self.file_name.setText(_translate("FileWidget", "TextLabel"))
        self.install_button.setText(_translate("FileWidget", "..."))

