# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/ProgressDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ProgressDialog(object):
    def setupUi(self, ProgressDialog):
        ProgressDialog.setObjectName("ProgressDialog")
        ProgressDialog.resize(400, 104)
        ProgressDialog.setMaximumSize(QtCore.QSize(16777215, 104))
        self.verticalLayout = QtWidgets.QVBoxLayout(ProgressDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.status_label = QtWidgets.QLabel(ProgressDialog)
        self.status_label.setMaximumSize(QtCore.QSize(16777215, 24))
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.status_label.setObjectName("status_label")
        self.verticalLayout.addWidget(self.status_label)
        self.progbar_1 = QtWidgets.QProgressBar(ProgressDialog)
        self.progbar_1.setProperty("value", 24)
        self.progbar_1.setObjectName("progbar_1")
        self.verticalLayout.addWidget(self.progbar_1)
        self.progbar_2 = QtWidgets.QProgressBar(ProgressDialog)
        self.progbar_2.setProperty("value", 24)
        self.progbar_2.setObjectName("progbar_2")
        self.verticalLayout.addWidget(self.progbar_2)

        self.retranslateUi(ProgressDialog)
        QtCore.QMetaObject.connectSlotsByName(ProgressDialog)

    def retranslateUi(self, ProgressDialog):
        _translate = QtCore.QCoreApplication.translate
        ProgressDialog.setWindowTitle(_translate("ProgressDialog", "ProgressDialog"))
        self.status_label.setText(_translate("ProgressDialog", "Initializing..."))

