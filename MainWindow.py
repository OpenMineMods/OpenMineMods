# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/untitled.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(790, 586)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.packs_installed = QtWidgets.QWidget()
        self.packs_installed.setObjectName("packs_installed")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.packs_installed)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tabWidget.addTab(self.packs_installed, "")
        self.packs_browse = QtWidgets.QWidget()
        self.packs_browse.setObjectName("packs_browse")
        self.tabWidget.addTab(self.packs_browse, "")
        self.gridLayout.addWidget(self.tabWidget, 2, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 790, 23))
        self.menubar.setObjectName("menubar")
        self.menuWhat_is_this = QtWidgets.QMenu(self.menubar)
        self.menuWhat_is_this.setObjectName("menuWhat_is_this")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuWhat_is_this.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.packs_installed), _translate("MainWindow", "Installed Packs"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.packs_browse), _translate("MainWindow", "Browse Packs"))
        self.menuWhat_is_this.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))

