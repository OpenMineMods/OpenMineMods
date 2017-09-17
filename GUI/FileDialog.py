# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/FileDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FileDialog(object):
    def setupUi(self, FileDialog):
        FileDialog.setObjectName("FileDialog")
        FileDialog.resize(400, 300)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(FileDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(FileDialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 380, 280))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.file_box = QtWidgets.QVBoxLayout()
        self.file_box.setObjectName("file_box")
        self.verticalLayout_3.addLayout(self.file_box)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)

        self.retranslateUi(FileDialog)
        QtCore.QMetaObject.connectSlotsByName(FileDialog)

    def retranslateUi(self, FileDialog):
        _translate = QtCore.QCoreApplication.translate
        FileDialog.setWindowTitle(_translate("FileDialog", "Dialog"))

