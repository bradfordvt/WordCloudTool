"""
@package wordcloudtool.qt5
@author Bradford G. Van Treuren
@copyright: Copyright (c) Bradford G. Van Treuren 2019. All rights reserved.
@version: 0.1
@change: Apr 03, 2019 - Initial release
GUI class for Qt5 based front end.
"""

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDesktopWidget, QApplication, qApp, QDialog, QFileDialog, QAbstractItemView
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QModelIndex
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QImage, QPixmap, QBrush, QColor
from PyQt5.QtCore import Qt

from PIL import Image
from PIL.ImageQt import ImageQt

from wordcloudtool.qt5.wordcloudtool_main import Ui_MainWindow  # importing our generated file
from wordcloudtool.qt5.wordcloudtool_about import Ui_DialogAbout
from wordcloudtool.qt5.GraphicsDisplay import Ui_DialogGraphicsDisplay

from wordcloudtool.control.StopWordsControl import StopWordsControl
from wordcloudtool.parser.TextFileParser import TextFileParser
from wordcloudtool.parser.URLParser import URLParser
from wordcloudtool.parser.TextWidgetParser import TextWidgetParser
from wordcloudtool.parser.PDFTextParser import PDFTextParser
from wordcloudtool.parser.PDFImageParser import PDFImageParser
from wordcloudtool.model.CloudWords import CloudWords
from wordcloudtool.model.WordCloudWrapper import WordCloudWrapper
from wordcloudtool.qt5.WordCloudDialog import WordCloudDialog
from wordcloudtool.qt5.WordHistogramDialog import WordHistogramDialog

import sys
import os

VERSION = "v0.1.0"
BUILDDATE = "20190411"


class WordCloudToolQt5View(QtWidgets.QMainWindow):
    def __init__(self):
        super(WordCloudToolQt5View, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.__center()
        self.version = VERSION
        self.builddate = BUILDDATE
        self.word_list = []
        self.__setupConnections()
        self.__setupStopWords()
        self.__setupImageObservers()
        self.__setupGraphicsViews()
        self.__setupDialogs()

    def __setupConnections(self):
        self.__setupMenuConnections()
        self.__setupButtonConnections()
        self.__setupComboBoxConnections()
        self.__setupLineEditsConnections()
        self.__setupListViewsConnections()
        self.__setupTextEditConnections()

    def __setupMenuConnections(self):
        self.ui.actionExit.triggered.connect(qApp.quit)
        self.ui.actionAbout.triggered.connect(self.__aboutEvent)
        self.ui.actionStart_Over.triggered.connect(self.__startOverEvent)

    def __setupButtonConnections(self):
        self.ui.pushButton_BrowseStopWordsFile.clicked.connect(self.__BrowseStopWordsFile)
        self.ui.pushButton_StopWordsEditorDelete.clicked.connect(self.__StopWordsEditorDelete)
        self.ui.pushButton_StopWordsEditorAdd.clicked.connect(self.__StopWordsEditorAdd)
        self.ui.pushButton_WordCloud.clicked.connect(self.__WordCloudInSeparateWindow)
        self.ui.pushButton_WordHistogram.clicked.connect(self.__WordHistogramInSeparateWindow)
        self.ui.pushButton_Visualize.clicked.connect(self.__Visualize)
        self.ui.pushButtonBrowseTextFile.clicked.connect(self.__BrowseTextFile)
        self.ui.pushButtonBrowsePDFFile.clicked.connect(self.__BrowsePDFFile)
        self.ui.pushButtonBrowseImageFile.clicked.connect(self.__BrowseImageFile)
        self.ui.pushButtonBrowseWordDoc.clicked.connect(self.__BrowseWordDoc)

    def __setupComboBoxConnections(self):
        self.ui.comboBox.currentTextChanged.connect(self.__ComboBoxChanged)

    def __setupStopWords(self):
        self.__updateStopWordsModel()
        stopwords_control = StopWordsControl.get_StopWordsControl()
        stopwords_control.register_observer(self.__observeStopWordsModelChanges)

    def __setupLineEditsConnections(self):
        self.ui.lineEdit_StopWordsFile.textChanged.connect(self.__StopFileChanged)
        self.ui.lineEdit_StopWordsEditorWord.textChanged.connect(self.__StopWordsEditorChanged)
        # From Text File Tab
        self.ui.lineEditTextFile.textChanged.connect(self.__processTextFile)
        # From URL Tab
        self.ui.lineEdit_WebPageURL.textChanged.connect(self.__processURL)
        # From PDF Text File Tab
        self.ui.lineEditPDFFile.textChanged.connect(self.__processPDFFile) # TODO - add __processPDFFile
        # From Image File Tab
        self.ui.lineEditImageFile.textChanged.connect(self.__processImageFile) # TODO - add __processImageFile
        # From Word Doc Tab
        self.ui.lineEditWordDoc.textChanged.connect(self.__processWordDoc) # TODO - add __processWordDoc

    def __setupListViewsConnections(self):
        self.ui.listViewStopWordsEditor.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.listview_model = QStandardItemModel()
        self.ui.listViewStopWordsEditor.clicked.connect(self.__StopWordsEditorSelected)

    def __setupTextEditConnections(self):
        self.ui.textEditPasteText.textChanged.connect(self.__processTextEdit)

    def __setupImageObservers(self):
        wrapper = WordCloudWrapper.get_WordCloudWrapper() # obtain Singleton of the wrapper
        wrapper.register_frequency_observer(self.__freqImageObserver)
        wrapper.register_image_observer(self.__cloudImageObserver)

    def __setupGraphicsViews(self):
        self.histogram_scene = QGraphicsScene()
        self.cloud_scene = QGraphicsScene()
        self.ui.graphicsView_WordHistogram.setScene(self.histogram_scene)
        self.ui.graphicsViewWordCloud.setScene(self.cloud_scene)

    def __setupDialogs(self):
        self.wordcloud_dialog = WordCloudDialog()
        self.wordhistogram_dialog = WordHistogramDialog()

    def __updateStopWordsModel(self):
        stopwords_control = StopWordsControl.get_StopWordsControl()
        wlist = []
        self.listview_model = QStandardItemModel()
        if self.ui.comboBox.currentText() == "Alphabetical":
            wlist = stopwords_control.get_alphabetic_stopwords()
            for w in wlist:
                self.listview_model.appendRow(QStandardItem(w))
            self.ui.listViewStopWordsEditor.setModel(self.listview_model)
        else:
            wlist = stopwords_control.get_unsorted_stopwords()
            for w in wlist:
                self.listview_model.appendRow(QStandardItem(w))
            self.ui.listViewStopWordsEditor.setModel(self.listview_model)

    def __center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def __getFileDialog(self, title, filter="All files (*.*)"):
        cwd = os.path.curdir
        fname = QFileDialog.getOpenFileName(self, title, cwd, filter)
        print("fname=({:s}, {:s})".format(fname[0], fname[1]))
        if fname[0] == "":
            return fname[0]
        return os.path.abspath(fname[0])

    def __observeStopWordsModelChanges(self, stopwords):
        self.__updateStopWordsModel()

    def __freqImageObserver(self, wrapper):
        print("In __freqImageObserver")
        self.ui.tabWidget_WordCloud.setCurrentIndex(1)
        image = wrapper.get_frequency_image()
        height, width, byteValue = image.shape
        byteValue = byteValue * width
        qimage = QImage(image, width, height, byteValue, QImage.Format_RGB888)
        pmap = QPixmap.fromImage(qimage)
        self.histogram_scene.addPixmap(pmap)
        self.histogram_scene.setBackgroundBrush(QBrush(QColor(0, 0, 0)))
        self.ui.graphicsView_WordHistogram.fitInView(0, 0, pmap.width(), pmap.height(), Qt.KeepAspectRatio)

    def __cloudImageObserver(self, wrapper):
        print("In __CloudImageObserver")
        self.ui.tabWidget_WordCloud.setCurrentIndex(0)
        image = wrapper.get_cloud_image()
        height, width, byteValue = image.shape
        byteValue = byteValue * width
        qimage = QImage(image, width, height, byteValue, QImage.Format_RGB888)
        pmap = QPixmap.fromImage(qimage)
        self.cloud_scene.addPixmap(pmap)
        self.cloud_scene.setBackgroundBrush(QBrush(QColor(0, 0, 0)))
        self.ui.graphicsViewWordCloud.fitInView(0, 0, pmap.width(), pmap.height(), Qt.KeepAspectRatio)

    @pyqtSlot()
    def __aboutEvent(self):
        DialogAbout = QDialog()
        ui = Ui_DialogAbout()
        ui.setupUi(DialogAbout)
        ui.lineEditVersion.setText(self.version)
        ui.lineEditBuildDate.setText(self.builddate)
        DialogAbout.show()
        rsp = DialogAbout.exec_()

    @pyqtSlot()
    def __startOverEvent(self):
        self.statusBar().showMessage('Starting over...')

    @pyqtSlot()
    def __BrowseStopWordsFile(self):
        print("BrowseStopWordsFile button clicked!")
        filepath = self.__getFileDialog("Select StopWords File")
        self.ui.lineEdit_StopWordsFile.setText(filepath)

    @pyqtSlot()
    def __StopWordsEditorAdd(self):
        print("StopWordsEditorAdd button clicked!")
        word = self.ui.lineEdit_StopWordsEditorWord.text()
        stopwords_controller = StopWordsControl.get_StopWordsControl()
        # Check to see if multiple words were entered
        words = word.split()
        if len(words) > 1:
            stopwords_controller.add_stopwords(words)
        else:
            stopwords_controller.add_stopword(word)

    @pyqtSlot()
    def __StopWordsEditorDelete(self):
        print("StopWordsEditorDelete button clicked!")
        word = self.ui.lineEdit_StopWordsEditorWord.text()
        stopwords_controller = StopWordsControl.get_StopWordsControl()
        # Check to see if multiple words were entered
        words = word.split()
        if len(words) > 1:
            stopwords_controller.remove_stopwords(words)
        else:
            stopwords_controller.remove_stopword(word)

    @pyqtSlot()
    def __WordCloudInSeparateWindow(self):
        print("WordCloudInSeparateWindow button clicked!")
        #Dialog = WordCloudDialog()
        # Dialog = QtWidgets.QDialog()
        # ui = Ui_DialogGraphicsDisplay()
        # ui.setupUi(Dialog)
        # Dialog.setWindowTitle("Word Cloud In a Separate Window")
        self.wordcloud_dialog.show()
        self.wordcloud_dialog.exec_()

    @pyqtSlot()
    def __WordHistogramInSeparateWindow(self):
        print("WordHistogramInSeparateWindow button clicked!")
        #Dialog = WordHistogramDialog()
        # Dialog = QtWidgets.QDialog()
        # ui = Ui_DialogGraphicsDisplay()
        # ui.setupUi(Dialog)
        # Dialog.setWindowTitle("Word Histogram In a Separate Window")
        self.wordhistogram_dialog.show()
        self.wordhistogram_dialog.exec_()

    @pyqtSlot()
    def __Visualize(self):
        print("Visualize button clicked!")
        stopfile_control = StopWordsControl.get_StopWordsControl()
        wrapper = WordCloudWrapper.get_WordCloudWrapper()
        wrapper.set_stopwords(stopfile_control.get_stopwords())
        cloud_words = CloudWords()
        cloud_words.add_words(self.word_list)
        word_count = cloud_words.get_word_count()
        wrapper.generate_from_count(word_count)

    @pyqtSlot()
    def __BrowseTextFile(self):
        print("BrowseTextFile button clicked!")
        filepath = self.__getFileDialog("Select Text File to process", filter="Text files (*.txt)")
        self.ui.lineEditTextFile.setText(filepath)

    @pyqtSlot()
    def __BrowsePDFFile(self):
        print("BrowsePDFFile button clicked!")
        filepath = self.__getFileDialog("Select PDF File to process", filter="PDF files (*.pdf)")
        self.ui.lineEditPDFFile.setText(filepath)

    @pyqtSlot()
    def __BrowseImageFile(self):
        print("BrowseImageFile button clicked!")
        type = self.ui.comboBoxImageFile.currentText()
        filepath = self.__getFileDialog("Select Image File to process", filter="Image file (*.{:s})".format(type))
        self.ui.lineEditImageFile.setText(filepath)

    @pyqtSlot()
    def __BrowseWordDoc(self):
        print("BrowseWorDoc button clicked!")
        filepath = self.__getFileDialog("Select Word Document File to process", filter="Document files (*.doc *.docx *.rtf)")
        self.ui.lineEditWordDoc.setText(filepath)

    @pyqtSlot()
    def __ComboBoxChanged(self):
        print("ComboBoxChanged!")
        print("ComboBox is now set to {:s}.".format(self.ui.comboBox.currentText()))
        self.__updateStopWordsModel()

    @pyqtSlot()
    def __StopFileChanged(self, text):
        stopfile_control = StopWordsControl.get_StopWordsControl()
        stopfile_control.set_stopfile(text)

    # @pyqtSlot()
    # def __StopWordsEditorChanged(self, text):
    #     print("StopWordsEditor changed to {:s}".format(text))
    #
    @pyqtSlot()
    def __StopWordsEditorChanged(self):
        text = self.ui.lineEdit_StopWordsEditorWord.text()
        print("StopWordsEditor changed to {:s}".format(text))

    @pyqtSlot()
    def __StopWordsEditorSelected(self):
        index = self.ui.listViewStopWordsEditor.currentIndex()
        print("StopWordsListView Selected a word")
        print(index.data())
        self.ui.lineEdit_StopWordsEditorWord.setText(index.data())

    @pyqtSlot()
    def __processTextFile(self):
        print("Calling __processTextFile")
        filename = self.ui.lineEditTextFile.text()
        if filename == "":
            return
        parser = TextFileParser(filename)
        self.word_list = parser.parse()

    @pyqtSlot()
    def __processURL(self):
        print("Calling __processURL")
        url = self.ui.lineEdit_WebPageURL.text()
        parser = URLParser(url)
        self.word_list = parser.parse()

    @pyqtSlot()
    def __processTextEdit(self):
        print("Calling __processTextEdit")
        text = self.ui.textEditPasteText.document().toPlainText()
        parser = TextWidgetParser(text)
        self.word_list = parser.parse()

    @pyqtSlot()
    def __processPDFFile(self):
        print("Calling __processPDFFile")
        filename = self.ui.lineEditPDFFile.text()
        if filename == "":
            return
        type = self.ui.comboBoxPDFFile.currentText()
        if type == "Text":
            parser = PDFTextParser(filename)
            self.word_list = parser.parse()
            if len(self.word_list) == 0:
                parser = PDFImageParser(filename)
                self.word_list = parser.parse()
        else:
            parser = PDFImageParser(filename)
            self.word_list = parser.parse()

    @pyqtSlot()
    def __processImageFile(self):
        print("Calling __processImageFile")
        filename = self.ui.lineEditImageFile.text()
        if filename == "":
            return
        # parser = TextFileParser(filename)
        # self.word_list = parser.parse()

    @pyqtSlot()
    def __processWordDoc(self):
        print("Calling __processWordDocFile")
        filename = self.ui.lineEditWordDoc.text()
        if filename == "":
            return
        # parser = TextFileParser(filename)
        # self.word_list = parser.parse()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = WordCloudToolQt5View()
    view.show()
    sys.exit(app.exec_())
