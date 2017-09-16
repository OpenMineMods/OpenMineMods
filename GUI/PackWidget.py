# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/PackWidget.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PackWidget(object):
    def setupUi(self, PackWidget):
        PackWidget.setObjectName("PackWidget")
        PackWidget.resize(455, 59)
        self.horizontalLayout = QtWidgets.QHBoxLayout(PackWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pack_name = QtWidgets.QLabel(PackWidget)
        self.pack_name.setObjectName("pack_name")
        self.horizontalLayout.addWidget(self.pack_name)
        self.pack_more = QtWidgets.QToolButton(PackWidget)
        icon = QtGui.QIcon.fromTheme("info")
        self.pack_more.setIcon(icon)
        self.pack_more.setObjectName("pack_more")
        self.horizontalLayout.addWidget(self.pack_more)
        self.pack_install = QtWidgets.QToolButton(PackWidget)
        icon = QtGui.QIcon.fromTheme("down")
        self.pack_install.setIcon(icon)
        self.pack_install.setObjectName("pack_install")
        self.horizontalLayout.addWidget(self.pack_install)

        self.retranslateUi(PackWidget)
        QtCore.QMetaObject.connectSlotsByName(PackWidget)

    def retranslateUi(self, PackWidget):
        _translate = QtCore.QCoreApplication.translate
        PackWidget.setWindowTitle(_translate("PackWidget", "Form"))
        self.pack_name.setText(_translate("PackWidget", "TextLabel"))
        self.pack_more.setText(_translate("PackWidget", "..."))
        self.pack_install.setText(_translate("PackWidget", "..."))

