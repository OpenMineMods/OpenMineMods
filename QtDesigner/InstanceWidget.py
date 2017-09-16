# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'instance_widget.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_instance_obj(object):
    def setupUi(self, instance_obj):
        instance_obj.setObjectName("instance_obj")
        instance_obj.resize(456, 48)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(instance_obj)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.instance_name = QtWidgets.QLabel(instance_obj)
        self.instance_name.setObjectName("instance_name")
        self.horizontalLayout.addWidget(self.instance_name)
        self.instance_delete = QtWidgets.QToolButton(instance_obj)
        icon = QtGui.QIcon.fromTheme("edit-delete")
        self.instance_delete.setIcon(icon)
        self.instance_delete.setObjectName("instance_delete")
        self.horizontalLayout.addWidget(self.instance_delete)
        self.instance_edit = QtWidgets.QToolButton(instance_obj)
        icon = QtGui.QIcon.fromTheme("edit")
        self.instance_edit.setIcon(icon)
        self.instance_edit.setObjectName("instance_edit")
        self.horizontalLayout.addWidget(self.instance_edit)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(instance_obj)
        QtCore.QMetaObject.connectSlotsByName(instance_obj)

    def retranslateUi(self, instance_obj):
        _translate = QtCore.QCoreApplication.translate
        instance_obj.setWindowTitle(_translate("instance_obj", "Form"))
        self.instance_name.setText(_translate("instance_obj", "TextLabel"))
        self.instance_delete.setText(_translate("instance_obj", "..."))
        self.instance_edit.setText(_translate("instance_obj", "..."))

