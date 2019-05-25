from wordcloudtool.qt5.WordCloudToolQt5View import WordCloudToolQt5View
from PyQt5.QtWidgets import QApplication
import sys


class Qt5GUIFactory(object):
    """
    Class to construct up the GUI frames in a Qt5 environment.
    """

    def make_gui(self):
        """
        Factory method for building the display.
        """
        app = QApplication(sys.argv)
        view = WordCloudToolQt5View()
        view.show()
        sys.exit(app.exec_())
