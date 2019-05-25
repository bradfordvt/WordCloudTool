# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GraphicsDisplay.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DialogGraphicsDisplay(object):
    def setupUi(self, DialogGraphicsDisplay):
        DialogGraphicsDisplay.setObjectName("DialogGraphicsDisplay")
        DialogGraphicsDisplay.resize(861, 687)
        self.widget = QtWidgets.QWidget(DialogGraphicsDisplay)
        self.widget.setGeometry(QtCore.QRect(5, 10, 851, 671))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.graphicsView = QtWidgets.QGraphicsView(self.widget)
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout.addWidget(self.graphicsView)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButtonWriteToFile = QtWidgets.QPushButton(self.widget)
        self.pushButtonWriteToFile.setObjectName("pushButtonWriteToFile")
        self.horizontalLayout.addWidget(self.pushButtonWriteToFile)
        spacerItem = QtWidgets.QSpacerItem(338, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonClose = QtWidgets.QPushButton(self.widget)
        self.pushButtonClose.setObjectName("pushButtonClose")
        self.horizontalLayout.addWidget(self.pushButtonClose)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(DialogGraphicsDisplay)
        QtCore.QMetaObject.connectSlotsByName(DialogGraphicsDisplay)

    def retranslateUi(self, DialogGraphicsDisplay):
        _translate = QtCore.QCoreApplication.translate
        DialogGraphicsDisplay.setWindowTitle(_translate("DialogGraphicsDisplay", "Dialog"))
        self.pushButtonWriteToFile.setText(_translate("DialogGraphicsDisplay", "Write to File"))
        self.pushButtonClose.setText(_translate("DialogGraphicsDisplay", "Close"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogGraphicsDisplay = QtWidgets.QDialog()
    ui = Ui_DialogGraphicsDisplay()
    ui.setupUi(DialogGraphicsDisplay)
    DialogGraphicsDisplay.show()
    sys.exit(app.exec_())
