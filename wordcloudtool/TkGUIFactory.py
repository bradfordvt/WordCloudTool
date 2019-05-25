#from wordcloudtool.tk.WordCloudParserTkView import WordCloudParserTkView
import sys


class TkGUIFactory(object):
    """
    Class to construct up the GUI frames in a Tk environment.
    """

    def make_gui(self):
        """
        Factory method for building the display.
        """
        raise NotImplementedError('Tk GUI is not yet implemented!')
        #app = QApplication(sys.argv)
        #view = WordCloudParserQt5View()
        #view.show()
        #sys.exit(app.exec_())
