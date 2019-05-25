"""
@package wordcloudtool.model
@author Bradford G. Van Treuren
@copyright: Copyright (c) Bradford G. Van Treuren 2019. All rights reserved.
@version: 0.1
@change: Mar 26, 2019 - Initial release
Specialized model class for providing source for words to remove from the list of words to cloudify.
"""
from wordcloud import STOPWORDS
import os


class StopWords(object):
    """
    Class to model the words to use for filtering out unwanted words when creating the word cloud.
    """
    def __init__(self):
        """
        Constructor
        """
        self.stopwords = set(STOPWORDS)
        self.stop_filename = ""
        self.observers = []

    def get_stopfile(self):
        return self.stop_filename

    def set_stopfile(self, filename):
        if os.path.exists(filename):
            self.stopwords = set(map(str.strip, open(os.path.abspath(filename)).readlines()))
            self.stop_filename = filename
        else:
            raise ValueError("{:s} stop file cannot be found!".format(filename))

    def get_stopwords(self):
        """
        Get the current set of stopwords.
        :return: A set of stopwords.
        """
        return self.stopwords

    def add_stopword(self, word):
        """
        Add a new stopword to the set of stopwords.
        :param word: A new word to add to the set of stop words.
        :return:
        """
        if word in self.stopwords:
            raise ValueError('{:s} was already added to stopwords.'.format(word))
        else:
            self.stopwords.add(word)
            self.__notify_observers()

    def add_stopwords(self, words):
        """
        Add a new set of stopwords to the set of stopwords.
        :param words: A set of new words to add to stopwords.
        :return:
        """
        for word in words:
            if word in self.stopwords:
                raise ValueError('{:s} was already added to stopwords.'.format(word))
            else:
                self.stopwords.add(word)
        self.__notify_observers()

    def del_stopword(self, word):
        """
        Removes a specific word from the set of stopwords.
        :param word: A string containing the word to remove.
        :return:
        """
        self.stopwords.remove(word)
        self.__notify_observers()

    def del_stopwords(self, words):
        """
        Removes a list of words from the list of stop words.
        :param words: A list of words to be removed from the stop words model.
        :return:
        """
        for word in words:
            if word in self.stopwords:
                self.stopwords.pop()
            else:
                raise ValueError('{:s} is not in the list.'.format(word))
        self.__notify_observers()

    def register_observer(self, observer):
        """
        Register a client that needs to be notified when the words for the stopwords has been updated.
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
        Utility to notify observers of a change to the words in the stopwords.
        Observers must have the signature where this instance is passed as the only argument.
        Example:
        StopView.stop_observer(stopwords)
        :return:
        """
        for observer in self.observers:
            observer(self)
