class WordCloudApplication(object):
    """
    Generic starting point for the application.
    Delegate to the GUI factory to create the user's view console.
    """

    def __init__(self):
        """
        Constructor
        """
        pass

    def make_gui(self, gui_factory=None):
        """
        Constructor
        :param gui_factory: Reference to the factory class building up the selected GUI interface
        """
        if gui_factory is None:
            raise AssertionError('A gui_factory must be defined!')
        return gui_factory().make_gui()
