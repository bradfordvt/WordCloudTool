"""
@package wordcloudtool.control
@author Bradford G. Van Treuren
@copyright: Copyright (c) Bradford G. Van Treuren 2019. All rights reserved.
@version: 0.1
@change: Mar 25, 2019 - Initial release
Class for controlling the words to be displayed on the word cloud.
This control is used by the view objects of the Model-View-Controller (MVC) architecture.
"""
from wordcloudtool.model.CloudWords import CloudWords


class CloudWordsControl(object):
    """
    Class for controlling the words to be displayed on the word cloud.
    """
    inst = None
    lock = True

    @staticmethod
    def get_CloudWordsControl():
        """
        Factory method for creating a single use instance (Singleton) of the control.
        :return:
        """
        if CloudWordsControl.inst is None:
            CloudWordsControl.lock = False  # workaround to create private constructor enforcement
            CloudWordsControl.inst = CloudWordsControl()
        return CloudWordsControl.inst

    def __init__(self):
        """
        Constructor
        """
        if CloudWordsControl.lock:
            raise AssertionError('CloudWordsControl.get_CloudWordsControl() must be called to create an instance.')
        self.model = CloudWords()
        CloudWordsControl.lock = True

    def add_word(self, word):
        """
        Adds a new word to the list of words to display. If the word was already added, it updates the count for
        the number of times that word is found.
        :param word: A string containing the word to be added to the cloud.
        :return:
        """
        self.model.add_word(word)

    def add_words(self, words):
        """
        Adds new words to the list of words to display.  If a word in the list is already added, it updates
        the count for the number of times that word is found.
        :param words: A list of words to be added to the cloud.
        :return:
        """
        self.model.add_words(words)

    def remove_word(self, word):
        """
        Removes the specified word from the list of cloud words.
        :param word: A string containing the word to remove.
        :return:
        """
        self.model.remove_word(word)

    def remove_words(self, words):
        """
        Removes a list of words from the list of cloud words.
        :param words: A list of words to be removed from the cloud.
        :return:
        """
        self.model.remove_words(words)

    def register_observer(self, observer):
        """
        Register a client that needs to be notified when the words for the cloud has been updated.
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

