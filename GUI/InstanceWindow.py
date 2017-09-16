# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/InstanceWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_InstanceWindow(object):
    def setupUi(self, InstanceWindow):
        InstanceWindow.setObjectName("InstanceWindow")
        InstanceWindow.resize(500, 400)
        InstanceWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(InstanceWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_settings = QtWidgets.QWidget()
        self.tab_settings.setObjectName("tab_settings")
        self.tabWidget.addTab(self.tab_settings, "")
        self.tab_mods = QtWidgets.QWidget()
        self.tab_mods.setObjectName("tab_mods")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_mods)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.mod_scroll = QtWidgets.QScrollArea(self.tab_mods)
        self.mod_scroll.setWidgetResizable(True)
        self.mod_scroll.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.mod_scroll.setObjectName("mod_scroll")
        self.fjhgdsf_2 = QtWidgets.QWidget()
        self.fjhgdsf_2.setGeometry(QtCore.QRect(0, 0, 458, 301))
        self.fjhgdsf_2.setObjectName("fjhgdsf_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.fjhgdsf_2)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.mod_box = QtWidgets.QVBoxLayout()
        self.mod_box.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.mod_box.setObjectName("mod_box")
        self.verticalLayout_5.addLayout(self.mod_box)
        self.mod_scroll.setWidget(self.fjhgdsf_2)
        self.verticalLayout_2.addWidget(self.mod_scroll)
        self.tabWidget.addTab(self.tab_mods, "")
        self.verticalLayout.addWidget(self.tabWidget)
        InstanceWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(InstanceWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 500, 26))
        self.menubar.setObjectName("menubar")
        InstanceWindow.setMenuBar(self.menubar)

        self.retranslateUi(InstanceWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(InstanceWindow)

    def retranslateUi(self, InstanceWindow):
        _translate = QtCore.QCoreApplication.translate
        InstanceWindow.setWindowTitle(_translate("InstanceWindow", "MainWindow"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_settings), _translate("InstanceWindow", "Settings"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_mods), _translate("InstanceWindow", "Mods"))

