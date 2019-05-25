"""
@package wordcloudtool.model
@author Bradford G. Van Treuren
@copyright: Copyright (c) Bradford G. Van Treuren 2019. All rights reserved.
@version: 0.1
@change: Mar 25, 2019 - Initial release
Class for managing the words to be displayed on the word cloud.
"""


class CloudWords(object):
    """
    Class for managing the words to be displayed on the word cloud.
    """
    def __init__(self):
        """
        Constructor
        """
        self.words = {}
        self.observers = []

    def add_word(self, word):
        """
        Adds a new word to the list of words to display. If the word was already added, it updates the count for
        the number of times that word is found.
        :param word: A string containing the word to be added to the cloud.
        :return:
        """
        word = word.lower()
        if word in self.words.keys():
            self.words[word] = self.words[word] + 1
        else:
            self.words.update({word: 1})
        self.__notify_observers()

    def add_words(self, words):
        """
        Adds new words to the list of words to display.  If a word in the list is already added, it updates
        the count for the number of times that word is found.
        :param words: A list of words to be added to the cloud.
        :return:
        """
        for word in words:
            word = word.lower()
            if word in self.words.keys():
                self.words[word] = self.words[word] + 1
            else:
                self.words.update({word: 1})
        self.__notify_observers()

    def remove_word(self, word):
        """
        Removes the specified word from the list of cloud words.
        :param word: A string containing the word to remove.
        :return:
        """
        word = word.lower()
        if word in self.words.keys():
            self.words.pop(word, None)
            self.__notify_observers()
        else:
            raise ValueError('{:s} is not in the list.'.format(word))

    def remove_words(self, words):
        """
        Removes a list of words from the list of cloud words.
        :param words: A list of words to be removed from the cloud.
        :return:
        """
        for word in words:
            word = word.lower()
            if word in self.words.keys():
                self.words.pop(word, None)
            else:
                raise ValueError('{:s} is not in the list.'.format(word))
        self.__notify_observers()

    def get_word_list(self):
        """
        Method to return the list of words to be displayed in the cloud.
        :return: the list of words for the cloud.
        """
        return self.words.keys()

    def get_word_count(self):
        """
        Method to return the dictionary of words and count of use.
        :return: the dictionary of words and count of use.
        """
        return self.words

    def register_observer(self, observer):
        """
        Register a client that needs to be notified when the words for the cloud has been updated.
        :param observer: Client method to be called when list has been updated.
        :return:
        """
        self.observers.append(observer)

    def unregister_observer(self, observer):
        """
        Unregister a client so it will no longer be notified of changes.
        :param observer: Client method to be removed from the list of observers.
        :return:
        """
        self.observers.remove(observer)

    def __notify_observers(self):
        """
        Utility to notify observers of a change to the words in the cloud.
        Observers must have the signature where this instance is passed as the only argument.
        Example:
        CloudView.cloud_observer(cloud_words)
        :return:
        """
        for observer in self.observers:
            observer(self)
