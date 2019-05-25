"""
@package wordcloudtool.parser
@author Bradford G. Van Treuren
@copyright: Copyright (c) Bradford G. Van Treuren 2019. All rights reserved.
@version: 0.1
@change: Mar 25, 2019 - Initial release
Base class for file based input decoders providing source for words to cloudify.
"""
from abc import ABCMeta, abstractmethod
from wordcloudtool.parser.ParserBase import ParserBase
import os


class FileParser(ParserBase):
    """
    Abstract base class for all file based input decoders specifying the minimal API to be supported.  Interface class.
    """
    __metaclass__ = ABCMeta

    def __init__(self, filename=None, stopwords=None, include_numbers=False, min_word_length=0):
        """
        Constructor
        """
        if filename is None:
            raise AssertionError('No filename was passed to the constructor.')
        self.filename = filename
        # self.fd = None
        super(FileParser, self).__init__(stopwords, include_numbers, min_word_length)
        if not os.path.exists(filename):
            raise IOError('{:s} does not exist!'.format(filename))

    # def open(self):
    #     """
    #     Opens the file to be parsed and returns the file descriptor to the opened file.
    #     :return: A file descriptor to the open file.  Otherwise, IOERROR is raised on failure.
    #     """
    #     self.fd = open(self.filename, 'rb')
    #     return self.fd
    #
    # def close(self):
    #     """
    #     Closes the file being parsed.
    #     """
    #     if self.fd is None:
    #         raise AssertionError('File was not previously opened before close() was called!')
    #     else:
    #         self.fd.close()
