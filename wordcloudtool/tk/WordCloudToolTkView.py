"""
Tk version of the GUI
"""

from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import ttk

from wordcloudtool.control.StopWordsControl import StopWordsControl
from wordcloudtool.parser.TextFileParser import TextFileParser
from wordcloudtool.parser.URLParser import URLParser
from wordcloudtool.parser.TextWidgetParser import TextWidgetParser
from wordcloudtool.parser.PDFTextParser import PDFTextParser
from wordcloudtool.parser.PDFImageParser import PDFImageParser
from wordcloudtool.model.CloudWords import CloudWords
from wordcloudtool.model.WordCloudWrapper import WordCloudWrapper

LARGE_FONT = ("Verdana", 12)
SMALL_FONT = ("Verdana", 6)
WIDTH = 680
HEIGHT = 650


class WordCloudToolTkView(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.text_plain_text = None
        self.entry_web_page_url = None
        self.entry_text_file = None
        self.entry_word_doc = None
        self.entry_pdf_file = None
        self.entry_image_file = None
        self.entry_stop_words_file = None
        self.combobox_pdf_type = None
        self.combobox_image_type = None
        self.word_cloud_canvas = None
        self.word_histogram_canvas = None
        self.entry_stop_words_editor = None
        self.listbox_stop_words_editor = None
        self.entry_stop_words_file = None
        self.word_source_tab_control = None
        self.stop_tab_control = None
        self.cloud_tab_control = None
        self.web_page_url_variable = None
        self.text_file_variable = None
        self.word_doc_variable = None
        self.pdf_file_variable = None
        self.image_file_variable = None
        self.stop_word_file_variable = None
        self.stop_word_editor_variable = None
        self.stop_word_list_variable = None
        self.init_window()
        self.__setupStopWords()

    def init_window(self):
        # changing the title of our master widget
        self.master.title("Word Cloud Tool")
        self.master.geometry("{}x{}".format(WIDTH, HEIGHT))
        self.__create_menu()
        self.__create_word_source()
        self.__create_stop_cloud_panel()
        self.__create_visualize_panel()

    def __create_menu(self):
        # creating a menu instance
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # create the file object)
        file = Menu(menu)

        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        file.add_command(label="Open", command=self.__open_event)
        file.add_command(label="Save", command=self.__save_event)
        file.add_command(label="Save As", command=self.__save_as_event)
        file.add_separator()
        file.add_command(label="Exit", command=self.__exit_event)

        # added "file" to our menu
        menu.add_cascade(label="File", menu=file)

        # create the tools object
        tools = Menu(menu)
        tools.add_command(label="Start Over", command=self.__start_over_event)

        # added "tools" to our menu
        menu.add_cascade(label="Tools", menu=tools)

        # create the help object
        _help = Menu(menu)
        _help.add_command(label="About", command=self.__about_event)

        # added "help" to our menu
        menu.add_cascade(label="Help", menu=help)

    def __create_word_source(self):
        word_source_frame = Frame(self.master)
        self.word_source_tab_control = ttk.Notebook(word_source_frame)
        self.__create_plain_text_tab(self.word_source_tab_control)
        self.__create_web_page_url_tab(self.word_source_tab_control)
        self.__create_text_file_tab(self.word_source_tab_control)
        self.__create_word_doc_tab(self.word_source_tab_control)
        self.__create_pdf_file_tab(self.word_source_tab_control)
        self.__create_image_file_tab(self.word_source_tab_control)
        self.word_source_tab_control.pack(expand=1, fill=BOTH)
        word_source_frame.grid(row=0, columnspan=2)
        self.word_source_tab_control.bind("<<NotebookTabChanged>>", self.__word_source_tab_changed)

    def __setupStopWords(self):
        self.__updateStopWordsModel()
        stopwords_control = StopWordsControl.get_StopWordsControl()
        stopwords_control.register_observer(self.__observeStopWordsModelChanges)

    def __create_plain_text_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text='Plain Text')
        label_plain_text_text = ttk.Label(tab, text="Paste text to be visualized:", font=LARGE_FONT)
        label_plain_text_text.pack()
        label_plain_text_req = ttk.Label(tab, text="plain text, 500 kilobyte max", font=SMALL_FONT)
        label_plain_text_req.pack()
        self.text_plain_text = Text(tab, height=15, width=80)
        self.text_plain_text.bind("<<Modified>>", self.__processTextEdit)
        self.text_plain_text.pack()

    def __create_web_page_url_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text='Web Page URL')
        label_web_page_url_url = ttk.Label(tab, text="Web page URL:")
        label_web_page_url_url.pack()
        label_web_page_url_ex = ttk.Label(tab, text="e.g. http://myblog.com\n", font=SMALL_FONT)
        label_web_page_url_ex.pack()
        self.web_page_url_variable = StringVar()
        self.entry_web_page_url = ttk.Entry(tab, textvariable=self.web_page_url_variable)
        self.web_page_url_variable.trace('w', self.__processURL)
        self.entry_web_page_url.pack(fill='x', padx=6)

    def __create_text_file_tab(self, tab_control):
        tab1 = ttk.Frame(tab_control)
        tab_control.add(tab1, text='Text File')
        label_text_file = ttk.Label(tab1, text="Select a file:")
        self.text_file_variable = StringVar()
        self.entry_text_file = ttk.Entry(tab1, width=60, textvariable=self.text_file_variable)
        self.text_file_variable.trace('w', self.__processTextFile)
        button_text_file = ttk.Button(tab1, text="Browse", command=self.__browse_text_file)
        label_text_file.grid(row=0, column=0)
        self.entry_text_file.grid(row=0, column=1, columnspan=2)
        button_text_file.grid(row=0, column=3)

    def __create_word_doc_tab(self, tab_control):
        tab1 = ttk.Frame(tab_control)
        tab_control.add(tab1, text='Word Doc')
        label_word_doc = ttk.Label(tab1, text="Select a file:")
        self.word_doc_variable = StringVar()
        self.entry_word_doc = ttk.Entry(tab1, width=60, textvariable=self.word_doc_variable)
        self.word_doc_variable.trace('w', self.__processWordDoc)
        button_word_doc = ttk.Button(tab1, text="Browse", command=self.__browse_word_doc)
        label_word_doc.grid(row=0, column=0)
        self.entry_word_doc.grid(row=0, column=1, columnspan=2)
        button_word_doc.grid(row=0, column=3)

    def __create_pdf_file_tab(self, tab_control):
        tab1 = ttk.Frame(tab_control)
        tab_control.add(tab1, text='PDF File')
        label_pdf_file = ttk.Label(tab1, text="Select a file:")
        self.pdf_file_variable = StringVar()
        self.entry_pdf_file = ttk.Entry(tab1, width=60, textvariable=self.pdf_file_variable)
        self.pdf_file_variable.trace('w', self.__processPDFFile)
        button_pdf_file = ttk.Button(tab1, text="Browse", command=self.__browse_pdf_file)
        label_pdf_file.grid(row=0, column=0)
        self.entry_pdf_file.grid(row=0, column=1, columnspan=2)
        button_pdf_file.grid(row=0, column=3)
        self.combobox_pdf_type = ttk.Combobox(tab1)
        self.combobox_pdf_type['values'] = ('PDF', 'Image')
        self.combobox_pdf_type.current(0)
        self.combobox_pdf_type.bind("<<ComboboxSelected>>", self.__combobox_pdf_type_changed)
        self.combobox_pdf_type.grid(row=1, column=1)

    def __create_image_file_tab(self, tab_control):
        tab1 = ttk.Frame(tab_control)
        tab_control.add(tab1, text='Image File')
        label_image_file = ttk.Label(tab1, text="Select a file:")
        self.entry_image_file = ttk.Entry(tab1, width=60)
        button_image_file = ttk.Button(tab1, text="Browse", command=self.__browse_image_file)
        label_image_file.grid(row=0, column=0)
        self.image_file_variable = StringVar()
        self.entry_image_file = ttk.Entry(tab1, width=60, textvariable=self.image_file_variable)
        self.image_file_variable.trace('w', self.__processImageFile)
        self.entry_image_file.grid(row=0, column=1, columnspan=2)
        button_image_file.grid(row=0, column=3)
        self.combobox_image_type = ttk.Combobox(tab1)
        self.combobox_image_type['values'] = ('PNG', 'JPEG', 'GIF', 'TIFF')
        self.combobox_image_type.current(0)
        self.combobox_image_type.bind("<<ComboboxSelected>>", self.__combobox_image_type_changed)
        self.combobox_image_type.grid(row=1, column=1)

    def __create_stop_cloud_panel(self):
        stop_cloud_frame = ttk.Frame(self.master)
        stop_panel = self.__create_stop_panel(stop_cloud_frame)
        cloud_panel = self.__create_cloud_panel(stop_cloud_frame)
        # Orient in the stop_cloud_frame
        stop_panel.grid(row=0, column=0)
        cloud_panel.grid(row=0, column=1)
        stop_cloud_frame.grid(row=1, columnspan=2)

    def __create_stop_panel(self, parent):
        self.stop_tab_control = ttk.Notebook(parent)
        self.__create_stop_words_file_tab(self.stop_tab_control)
        self.__create_stop_words_editor_tab(self.stop_tab_control)
        self.stop_tab_control.bind("<<NotebookTabChanged>>", self.__stop_tab_changed)
        return self.stop_tab_control

    def __create_stop_words_file_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text='Stop Words File')
        label = ttk.Label(tab, text="Select the file containing your Stop Words:")
        label.pack()
        self.stop_word_file_variable = StringVar()
        self.entry_stop_words_file = ttk.Entry(tab, textvariable=self.stop_word_file_variable)
        self.stop_word_file_variable.trace('w', self.__StopFileChanged)
        self.entry_stop_words_file.pack(fill=X)
        button_stop_words_file = ttk.Button(tab, text="Browse", command=self.__browse_stop_words_file)
        button_stop_words_file.pack()

    def __create_stop_words_editor_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text='Stop Words Editor')
        label = ttk.Label(tab, text="Choose the sorting preference:")
        label.grid(row=0, columnspan=2)
        frame1 = ttk.Frame(tab)
        frame1.grid(row=1, column=0)
        self.combobox_stop_words_editor = ttk.Combobox(frame1)
        self.combobox_stop_words_editor['values'] = ('Alphabetic', 'Usage')
        self.combobox_stop_words_editor.current(0)
        self.combobox_stop_words_editor.bind("<<ComboboxSelected>>", self.__combobox_stop_words_editor_changed)
        self.combobox_stop_words_editor.grid(row=0, column=0)
        scrollbar = Scrollbar(frame1, orient="vertical")
        self.stop_word_list_variable = StringVar()
        self.listbox_stop_words_editor = Listbox(frame1,
                                                 selectmode=SINGLE,
                                                 yscrollcommand=scrollbar.set,
                                                 listvariable=self.stop_word_list_variable)
        self.listbox_stop_words_editor.grid(row=1, column=0)
        frame2 = ttk.Frame(tab)
        frame2.grid(row=1, column=1)
        button_add_stop_word = ttk.Button(frame2, text="Add Word", command=self.__StopWordsEditorAdd)
        button_add_stop_word.grid(row=0, column=0)
        label2 = ttk.Label(frame2, text="Selected Word:")
        label2.grid(row=1, column=0)
        self.stop_word_editor_variable = StringVar()
        self.entry_stop_words_editor = ttk.Entry(frame2, textvariable=self.stop_word_editor_variable)
        self.stop_word_editor_variable.trace('w', self.__StopWordsEditorChanged)
        self.entry_stop_words_editor.grid(row=2, column=0)
        button_delete_stop_word = ttk.Button(frame2, text="Delete Word", command=self.__StopWordsEditorDelete)
        button_delete_stop_word.grid(row=3, column=0)

    def __create_cloud_panel(self, parent):
        self.cloud_tab_control = ttk.Notebook(parent)
        self.__create_word_cloud_tab(self.cloud_tab_control)
        self.__create_word_histogram_tab(self.cloud_tab_control)
        self.cloud_tab_control.bind("<<NotebookTabChanged>>", self.__cloud_tab_changed)
        return self.cloud_tab_control

    def __create_word_cloud_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text='Word Cloud')
        label = ttk.Label(tab, text="Word Cloud View")
        label.pack()
        self.word_cloud_canvas = Canvas(tab, width=300, height=200, bg='black')
        self.word_cloud_canvas.pack()
        button_stop_words_file = ttk.Button(tab, text="Show Word Cloud in Separate Window", command=self.__WordCloudInSeparateWindow)
        button_stop_words_file.pack()

    def __create_word_histogram_tab(self, tab_control):
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text='Word Histogram')
        label = ttk.Label(tab, text="Word Histogram View")
        label.grid(row=0, columnspan=2)
        self.word_histogram_canvas = Canvas(tab, width=300, height=200, bg='black')
        self.word_histogram_canvas.grid(row=1, columnspan=2)
        button_histogram = ttk.Button(tab, text="Show Histogram in Separate Window", command=self.__WordHistogramInSeparateWindow)
        button_histogram.grid(row=2, column=0)

    def __create_visualize_panel(self):
        frame = ttk.Frame(self.master)
        frame.grid(row=3, columnspan=2)
        button_visualize = ttk.Button(frame, text="Visualize!", command=self.__button_visualize_clicked)
        button_visualize.grid(row=0, column=0)

    def __updateStopWordsModel(self):
        # TODO - Fix update of stop words list graphic
        stopwords_control = StopWordsControl.get_StopWordsControl()
        wlist = []
        slist = ""
        if self.combobox_stop_words_editor.get() == "Alphabetical":
            wlist = stopwords_control.get_alphabetic_stopwords()
            for w in wlist:
                slist = slist + ' ' + w
            self.stop_word_list_variable.set(slist)
        else:
            wlist = stopwords_control.get_unsorted_stopwords()
            for w in wlist:
                slist = slist + ' ' + w
            self.stop_word_list_variable.set(slist)

    def __open_event(self):
        print('Open menu called')

    def __save_event(self):
        print('Save menu called')

    def __save_as_event(self):
        print('Save As menu called')

    def __exit_event(self):
        print('Exit menu called')
        exit()

    def __start_over_event(self):
        print('Start over menu called')

    def __about_event(self):
        print('About menu called')

    def __browse_text_file(self):
        print("BrowseTextFile button clicked!")
        filepath = askopenfilename(filetypes=(("Text File", "*.txt"),),
                                   title="Select Text File to process"
                                   )
        self.entry_text_file.delete(0, END)
        self.entry_text_file.insert(0, filepath)

    def __browse_word_doc(self):
        print("BrowseWordDoc button clicked!")
        filepath = askopenfilename(filetypes=(("Doc File", "*.doc"), ("Doc File", "*.docx")),
                                   title="Select Word Document to process"
                                   )
        self.entry_word_doc.delete(0, END)
        self.entry_word_doc.insert(0, filepath)

    def __browse_pdf_file(self):
        print("BrowsePDFFile button clicked!")
        filepath = askopenfilename(filetypes=(("PDF File", "*.pdf"),),
                                   title="Select PDF File to process"
                                   )
        self.entry_pdf_file.delete(0, END)
        self.entry_pdf_file.insert(0, filepath)

    def __browse_image_file(self):
        print("BrowseTextFile button clicked!")
        filepath = askopenfilename(filetypes=(("PNG Image File", "*.png"),
                                              ("JPEG Image File", "*.jpeg"),
                                              ("JPEG Image File", "*.jpg"),
                                              ("GIF Image File", "*.gif"),
                                              ("TIFF Image File", "*.tiff")),
                                   title="Select Image File to process"
                                   )
        self.entry_image_file.delete(0, END)
        self.entry_image_file.insert(0, filepath)

    def __browse_stop_words_file(self):
        print("BrowseStopWordsFile button clicked!")
        filepath = askopenfilename(filetypes=(("Text File", "*.txt"),),
                                   title="Select File to process"
                                   )
        self.entry_pdf_file.delete(0, END)
        self.entry_pdf_file.insert(0, filepath)

    def __combobox_pdf_type_changed(self, event):
        print("ComboboxPDFType changed to {:s}!".format(self.combobox_pdf_type.get()))

    def __combobox_image_type_changed(self, event):
        print("ComboboxImageType changed to {:s}!".format(self.combobox_image_type.get()))

    def __WordCloudInSeparateWindow(self):
        print("WordCloudInSeparateWindow button clicked!")
        #Dialog = WordCloudDialog()
        # Dialog = QtWidgets.QDialog()
        # ui = Ui_DialogGraphicsDisplay()
        # ui.setupUi(Dialog)
        # Dialog.setWindowTitle("Word Cloud In a Separate Window")
        self.wordcloud_dialog.show()
        self.wordcloud_dialog.exec_()

    def __WordHistogramInSeparateWindow(self):
        print("WordHistogramInSeparateWindow button clicked!")
        #Dialog = WordHistogramDialog()
        # Dialog = QtWidgets.QDialog()
        # ui = Ui_DialogGraphicsDisplay()
        # ui.setupUi(Dialog)
        # Dialog.setWindowTitle("Word Histogram In a Separate Window")
        self.wordhistogram_dialog.show()
        self.wordhistogram_dialog.exec_()

    def __combobox_stop_words_editor_changed(self, event):
        print("Stop Words Editor Combobox changed to {:s}!".format(self.combobox_stop_words_editor.get()))

    def __StopFileChanged(self, text):
        stopfile_control = StopWordsControl.get_StopWordsControl()
        stopfile_control.set_stopfile(self.stop_word_file_variable)

    def __StopWordsEditorAdd(self):
        print("StopWordsEditorAdd button clicked!")
        word = self.stop_word_editor_variable
        stopwords_controller = StopWordsControl.get_StopWordsControl()
        # Check to see if multiple words were entered
        words = word.split()
        if len(words) > 1:
            stopwords_controller.add_stopwords(words)
        else:
            stopwords_controller.add_stopword(word)

    def __StopWordsEditorDelete(self):
        print("StopWordsEditorDelete button clicked!")
        word = self.stop_word_editor_variable
        stopwords_controller = StopWordsControl.get_StopWordsControl()
        # Check to see if multiple words were entered
        words = word.split()
        if len(words) > 1:
            stopwords_controller.remove_stopwords(words)
        else:
            stopwords_controller.remove_stopword(word)

    def __button_visualize_clicked(self):
        print("Visualize! button clicked!")

    def __word_source_tab_changed(self, event):
        current_tab = self.word_source_tab_control.tab("current")
        value = current_tab["text"]
        print("Word Source tab changed to {:s}!".format(value))

    def __stop_tab_changed(self, event):
        current_tab = self.stop_tab_control.tab("current")
        value = current_tab["text"]
        print("Stop tab changed to {:s}!".format(value))

    def __cloud_tab_changed(self, event):
        current_tab = self.cloud_tab_control.tab("current")
        value = current_tab["text"]
        print("Cloud tab changed to {:s}!".format(value))

    def __processTextFile(self, event):
        print("Calling __processTextFile")
        filename = self.text_file_variable
        if filename == "":
            return
        parser = TextFileParser(filename)
        self.word_list = parser.parse()

    def __processURL(self, event):
        print("Calling __processURL")
        url = self.web_page_url_variable
        parser = URLParser(url)
        self.word_list = parser.parse()

    def __processTextEdit(self, event):
        print("Calling __processTextEdit")
        text = self.text_plain_text.get(1.0, END)
        parser = TextWidgetParser(text)
        self.word_list = parser.parse()

    def __processPDFFile(self):
        print("Calling __processPDFFile")
        filename = self.pdf_file_variable
        if filename == "":
            return
        type = self.combobox_pdf_type.get()
        if type == "Text":
            parser = PDFTextParser(filename)
            self.word_list = parser.parse()
            if len(self.word_list) == 0:
                parser = PDFImageParser(filename)
                self.word_list = parser.parse()
        else:
            parser = PDFImageParser(filename)
            self.word_list = parser.parse()

    def __processImageFile(self):
        print("Calling __processImageFile")
        filename = self.image_file_variable
        if filename == "":
            return
        # parser = TextFileParser(filename)
        # self.word_list = parser.parse()

    def __processWordDoc(self):
        print("Calling __processWordDocFile")
        filename = self.word_doc_variable
        if filename == "":
            return
        # parser = TextFileParser(filename)
        # self.word_list = parser.parse()

    def __StopFileChanged(self, event):
        stopfile_control = StopWordsControl.get_StopWordsControl()
        stopfile_control.set_stopfile(self.stop_word_file_variable)

    def __StopWordsEditorChanged(self, event):
        text = self.stop_word_editor_variable
        print("StopWordsEditor changed to {:s}".format(text))

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


if __name__ == '__main__':
    root = Tk()
    app = WordCloudToolTkView(root)
    root.mainloop()
