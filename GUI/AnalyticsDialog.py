# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI/AnalyticsDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AnalyticsDialog(object):
    def setupUi(self, AnalyticsDialog):
        AnalyticsDialog.setObjectName("AnalyticsDialog")
        AnalyticsDialog.resize(394, 123)
        self.verticalLayout = QtWidgets.QVBoxLayout(AnalyticsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textBrowser = QtWidgets.QTextBrowser(AnalyticsDialog)
        self.textBrowser.setOpenExternalLinks(True)
        self.textBrowser.setOpenLinks(False)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.buttonBox = QtWidgets.QDialogButtonBox(AnalyticsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.No|QtWidgets.QDialogButtonBox.Yes)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(AnalyticsDialog)
        self.buttonBox.accepted.connect(AnalyticsDialog.accept)
        self.buttonBox.rejected.connect(AnalyticsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AnalyticsDialog)

    def retranslateUi(self, AnalyticsDialog):
        _translate = QtCore.QCoreApplication.translate
        AnalyticsDialog.setWindowTitle(_translate("AnalyticsDialog", "Dialog"))
        self.textBrowser.setHtml(_translate("AnalyticsDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Noto Sans CJK JP\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Would you like to enable basic analytics?</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"https://github.com/joonatoona/OpenMineMods/blob/master/ExampleAnalytics.md\"><span style=\" text-decoration: underline; color:#0000ff;\">More Info</span></a></p></body></html>"))

