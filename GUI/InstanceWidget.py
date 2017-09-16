# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/InstanceWidget.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_InstanceWidget(object):
    def setupUi(self, InstanceWidget):
        InstanceWidget.setObjectName("InstanceWidget")
        InstanceWidget.resize(400, 41)
        self.horizontalLayout = QtWidgets.QHBoxLayout(InstanceWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.instance_name = QtWidgets.QLabel(InstanceWidget)
        self.instance_name.setObjectName("instance_name")
        self.horizontalLayout.addWidget(self.instance_name)
        self.instance_delete = QtWidgets.QToolButton(InstanceWidget)
        icon = QtGui.QIcon.fromTheme("edit-delete")
        self.instance_delete.setIcon(icon)
        self.instance_delete.setObjectName("instance_delete")
        self.horizontalLayout.addWidget(self.instance_delete)
        self.instance_edit = QtWidgets.QToolButton(InstanceWidget)
        icon = QtGui.QIcon.fromTheme("edit")
        self.instance_edit.setIcon(icon)
        self.instance_edit.setObjectName("instance_edit")
        self.horizontalLayout.addWidget(self.instance_edit)

        self.retranslateUi(InstanceWidget)
        QtCore.QMetaObject.connectSlotsByName(InstanceWidget)

    def retranslateUi(self, InstanceWidget):
        _translate = QtCore.QCoreApplication.translate
        InstanceWidget.setWindowTitle(_translate("InstanceWidget", "Form"))
        self.instance_name.setText(_translate("InstanceWidget", "TextLabel"))
        self.instance_delete.setText(_translate("InstanceWidget", "..."))
        self.instance_edit.setText(_translate("InstanceWidget", "..."))

