# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wordcloudparser_about.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DialogAbout(object):
    def setupUi(self, DialogAbout):
        DialogAbout.setObjectName("DialogAbout")
        DialogAbout.resize(400, 278)
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogAbout)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.groupBoxDescription = QtWidgets.QGroupBox(DialogAbout)
        self.groupBoxDescription.setGeometry(QtCore.QRect(18, 99, 361, 131))
        self.groupBoxDescription.setObjectName("groupBoxDescription")
        self.scrollArea = QtWidgets.QScrollArea(self.groupBoxDescription)
        self.scrollArea.setGeometry(QtCore.QRect(0, 20, 361, 111))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 359, 109))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.textEditDescription = QtWidgets.QTextEdit(self.scrollAreaWidgetContents)
        self.textEditDescription.setEnabled(True)
        self.textEditDescription.setGeometry(QtCore.QRect(0, 0, 361, 111))
        self.textEditDescription.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.textEditDescription.setPlaceholderText("")
        self.textEditDescription.setObjectName("textEditDescription")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.widget = QtWidgets.QWidget(DialogAbout)
        self.widget.setGeometry(QtCore.QRect(40, 20, 204, 27))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelVersion = QtWidgets.QLabel(self.widget)
        self.labelVersion.setObjectName("labelVersion")
        self.horizontalLayout.addWidget(self.labelVersion)
        self.lineEditVersion = QtWidgets.QLineEdit(self.widget)
        self.lineEditVersion.setEnabled(True)
        self.lineEditVersion.setReadOnly(True)
        self.lineEditVersion.setObjectName("lineEditVersion")
        self.horizontalLayout.addWidget(self.lineEditVersion)
        self.widget1 = QtWidgets.QWidget(DialogAbout)
        self.widget1.setGeometry(QtCore.QRect(20, 67, 223, 27))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.labelBuildDate = QtWidgets.QLabel(self.widget1)
        self.labelBuildDate.setObjectName("labelBuildDate")
        self.horizontalLayout_2.addWidget(self.labelBuildDate)
        self.lineEditBuildDate = QtWidgets.QLineEdit(self.widget1)
        self.lineEditBuildDate.setEnabled(True)
        self.lineEditBuildDate.setReadOnly(True)
        self.lineEditBuildDate.setObjectName("lineEditBuildDate")
        self.horizontalLayout_2.addWidget(self.lineEditBuildDate)

        self.retranslateUi(DialogAbout)
        self.buttonBox.accepted.connect(DialogAbout.accept)
        self.buttonBox.rejected.connect(DialogAbout.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogAbout)

    def retranslateUi(self, DialogAbout):
        _translate = QtCore.QCoreApplication.translate
        DialogAbout.setWindowTitle(_translate("DialogAbout", "WordCloud Tool - About"))
        self.groupBoxDescription.setTitle(_translate("DialogAbout", "Description"))
        self.textEditDescription.setDocumentTitle(_translate("DialogAbout", "This is the documentTitle"))
        self.textEditDescription.setHtml(_translate("DialogAbout", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><title>This is the documentTitle</title><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Word Cloud Parser is used to parse documents and locate the frequency (count) of words used in the document.  The display of frequency of words is shown using a Word Cloud and a Word Histogram for the top frequency words.</p></body></html>"))
        self.labelVersion.setText(_translate("DialogAbout", "Version:"))
        self.labelBuildDate.setText(_translate("DialogAbout", "Build Date:"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogAbout = QtWidgets.QDialog()
    ui = Ui_DialogAbout()
    ui.setupUi(DialogAbout)
    DialogAbout.show()
    sys.exit(app.exec_())
