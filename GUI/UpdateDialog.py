# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/UpdateDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_UpdateDialog(object):
    def setupUi(self, UpdateDialog):
        UpdateDialog.setObjectName("UpdateDialog")
        UpdateDialog.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(UpdateDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(UpdateDialog)
        self.label.setAutoFillBackground(False)
        self.label.setStyleSheet("font-size: 16px;")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.textBrowser = QtWidgets.QTextBrowser(UpdateDialog)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.label_2 = QtWidgets.QLabel(UpdateDialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(UpdateDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.No|QtWidgets.QDialogButtonBox.Yes)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(UpdateDialog)
        self.buttonBox.accepted.connect(UpdateDialog.accept)
        self.buttonBox.rejected.connect(UpdateDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(UpdateDialog)

    def retranslateUi(self, UpdateDialog):
        _translate = QtCore.QCoreApplication.translate
        UpdateDialog.setWindowTitle(_translate("UpdateDialog", "Dialog"))
        self.label.setText(_translate("UpdateDialog", "An update for OpenMineMods is availible!"))
        self.label_2.setText(_translate("UpdateDialog", "Would you like to automatically install the update?"))

