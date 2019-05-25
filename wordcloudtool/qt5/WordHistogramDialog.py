"""
@package wordcloudtool.qt5
@author Bradford G. Van Treuren
@copyright: Copyright (c) Bradford G. Van Treuren 2019. All rights reserved.
@version: 0.1
@change: Apr 11, 2019 - Initial release
GUI class for Qt5 display of the Word Histogram in a separate window.
"""

from PyQt5.QtWidgets import QDialog, QDesktopWidget, QGraphicsScene, QFileDialog
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QModelIndex
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QImage, QPixmap, QBrush, QColor

from wordcloudtool.qt5.GraphicsDisplay import Ui_DialogGraphicsDisplay
from wordcloudtool.model.WordCloudWrapper import WordCloudWrapper

import os


class WordHistogramDialog(QDialog):
    def __init__(self):
        super(WordHistogramDialog, self).__init__()
        self.ui = Ui_DialogGraphicsDisplay()
        self.ui.setupUi(self)
        self.__setupConnections()
        self.__setupImageObservers()
        self.__setupGraphicsViews()
        self.setWindowTitle("Word Histogram In a Separate Window")
        self.pmap = None

    def __setupConnections(self):
        self.__setupButtonConnections()

    def __setupButtonConnections(self):
        self.ui.pushButtonWriteToFile.clicked.connect(self.__WriteToFile)
        self.ui.pushButtonClose.clicked.connect(self.__CloseWindow)

    def __setupImageObservers(self):
        wrapper = WordCloudWrapper.get_WordCloudWrapper() # Get Singleton of the wrapper
        wrapper.register_image_observer(self.__ImageObserver)

    def __setupGraphicsViews(self):
        self.scene = QGraphicsScene()
        self.ui.graphicsView.setScene(self.scene)

    def __center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def __getFileDialog(self, title):
        cwd = os.path.curdir
        fname = QFileDialog.getOpenFileName(self, title, cwd)
        print("fname=({:s}, {:s})".format(fname[0], fname[1]))
        if fname[0] == "":
            return fname[0]
        return os.path.abspath(fname[0])

    def __ImageObserver(self, wrapper):
        print("In __ImageObserver")
        image = wrapper.get_frequency_image()
        height, width, byteValue = image.shape
        byteValue = byteValue * width
        qimage = QImage(image, width, height, byteValue, QImage.Format_RGB888)
        pmap = QPixmap.fromImage(qimage)
        self.scene.addPixmap(pmap)
        self.scene.setBackgroundBrush(QBrush(QColor(0, 0, 0)))
        rect = pmap.rect()
        if not rect.isNull():
            self.ui.graphicsView.setSceneRect(QRectF(rect))

    @pyqtSlot()
    def __WriteToFile(self):
        print("WriteToFile button clicked!")
        filepath = self.__getFileDialog("Select Image File Name to write to")
        if os.path.exists(filepath):
            self.__saveFile(filepath)
        else:
            buttonReply = QMessageBox.question(self, 'File Creation Verification', "Do you want to write\n{:s}?".format(filepath),
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                print('Yes clicked.')
                # Save the image as a new file
                self.__saveFile(filepath)
            else:
                print('No clicked.')

    @pyqtSlot()
    def __CloseWindow(self):
        print("CloseWindow button clicked!")
        self.close()

    def __saveFile(self, filepath):
        print("In __saveFile()")
        if self.pmap is not None:
            image = self.pmap.toImage()
            image.save(filepath)
        else:
            QMessageBox.critical(self, 'Image is not displayed!', 'No image is displayed for application to save.', QMessageBox.Ok)
