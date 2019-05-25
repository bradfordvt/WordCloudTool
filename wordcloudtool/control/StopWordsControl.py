"""
@package wordcloudtool.control
@author Bradford G. Van Treuren
@copyright: Copyright (c) Bradford G. Van Treuren 2019. All rights reserved.
@version: 0.1
@change: Apr 8, 2019 - Initial release
Class for controlling the words to be eliminated from the word cloud.
This control is used by the view objects of the Model-View-Controller (MVC) architecture.
"""
from wordcloudtool.model.StopWords import StopWords


class StopWordsControl(object):
    """
    Class for controlling the words to be displayed on the word cloud.
    """
    inst = None
    lock = True

    @staticmethod
    def get_StopWordsControl():
        """
        Factory method for creating a single use instance (Singleton) of the control.
        :return:
        """
        if StopWordsControl.inst is None:
            StopWordsControl.lock = False  # workaround to create private constructor enforcement
            StopWordsControl.inst = StopWordsControl()
        return StopWordsControl.inst

    def __init__(self):
        """
        Constructor
        """
        if StopWordsControl.lock:
            raise AssertionError('StopWordsControl.get_StopWordsControl() must be called to create an instance.')
        self.model = StopWords()
        StopWordsControl.lock = True

    def add_stopword(self, word):
        """
        Adds a new word to the list of words to remove. If the word was already added, it ignores the word.
        :param word: A string containing the word to be added to the stop cloud.
        :return:
        """
        self.model.add_stopword(word)

    def add_stopwords(self, words):
        """
        Adds new words to the list of words to display.  If a word in the list is already added, it updates
        the count for the number of times that word is found.
        :param words: A list of words to be added to the cloud.
        :return:
        """
        self.model.add_stopwords(words)

    def remove_stopword(self, word):
        """
        Removes the specified word from the list of cloud words.
        :param word: A string containing the word to remove.
        :return:
        """
        self.model.del_stopword(word)

    def remove_stopwords(self, words):
        """
        Removes a list of words from the list of cloud words.
        :param words: A list of words to be removed from the cloud.
        :return:
        """
        self.model.del_stopwords(words)

    def set_stopfile(self, filename):
        self.model.set_stopfile(filename)

    def get_stopfile(self):
        return self.model.get_stopfile()

    def get_alphabetic_stopwords(self):
        return sorted(self.model.get_stopwords())

    def get_unsorted_stopwords(self):
        return self.model.get_stopwords()

    def get_stopwords(self):
        return self.model

    def register_observer(self, observer):
        """
        Register a client that needs to be notified when the stop words for the cloud has been updated.
        :param observer: Client method to be called when list has been updated.
        :return:
        """
        self.model.register_observer(observer)

    def unregister_observer(self, observer):
        """
        Unregister a client so it will no longer be notified of changes.
        :param observer: Client method to be removed from the list of observers.
        :return:
        """
        self.model.unregister_observer(observer)

