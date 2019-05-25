"""
@package wordcloudtool.parser
@author Bradford G. Van Treuren
@copyright: Copyright (c) Bradford G. Van Treuren 2019. All rights reserved.
@version: 0.1
@change: Mar 25, 2019 - Initial release
Base class for input decoders providing source for words to cloudify.
"""
from abc import ABCMeta, abstractmethod
import os

FILE = os.path.dirname(__file__)
STOPWORDS = set(map(str.strip, open(os.path.join(FILE, 'stopwords')).readlines()))


class ParserBase(object):
    """
    Abstract base class for all input decoders specifying the minimal API to be supported.  Interface class.
    """
    __metaclass__ = ABCMeta

    def __init__(self, stopwords=None, include_numbers=False, min_word_length=0):
        """
        Constructor
        """
        self.stopwords = stopwords if stopwords is not None else STOPWORDS
        self.include_numbers = include_numbers
        self.min_word_length = min_word_length

    def prune(self, words, stopwords=None):
        """
        Eliminate unwanted words from the list of words.
        """
        self.stopwords = stopwords if stopwords is not None else self.stopwords
        stopwords = set([i.lower() for i in self.stopwords])
        # remove stopwords
        words = [word for word in words if word.lower() not in stopwords]
        # remove 's
        words = [word[:-2] if word.lower().endswith("'s") else word
                 for word in words]
        # remove numbers
        if not self.include_numbers:
            words = [word for word in words if not word.isdigit()]
        # remove short words
        if self.min_word_length:
            words = [word for word in words if len(word) >= self.min_word_length]
        return words

    @abstractmethod
    def parse(self):
        """
        Abstract method defining interface to process the input file data and decode it into word tokens.
        :return:
        """
        raise NotImplementedError('Derived classes must implement the parse( ) method to decode the input data.')
