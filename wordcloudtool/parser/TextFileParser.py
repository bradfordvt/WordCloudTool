"""
@package wordcloudtool.parser
@author Bradford G. Van Treuren
@copyright: Copyright (c) Bradford G. Van Treuren 2019. All rights reserved.
@version: 0.1
@change: Mar 25, 2019 - Initial release
Specialized class for text file based input decoders providing source for words to cloudify.
"""
from wordcloudtool.parser.FileParser import FileParser
import re


class TextFileParser(FileParser):
    """
    Specialized class for text file based input decoders.
    """
    def __init__(self, filename=None):
        """
        Constructor
        :param filename: Name of the text file to parse.
        """
        self.regexp = None
        super(TextFileParser, self).__init__(filename)
        if not self.__test_for_text():
            raise IOError('{:s} is not a text file.'.format(filename))

    def parse(self):
        """
        Parse the contents of the text file and extract all the words into a list.
        :return: A list of words from the text file.
        """
        with open(self.filename, 'r') as f:
            ret = []
            for line in f:
                ret += self.__process_line(line)
            return ret

    def __process_line(self, line):
        """
        Process the contents of the line to strip out non-word characters and return a list of words.
        :param line: A string containing the characters from the line of the text file.
        :return: A list of words.
        """
        regexp = self.regexp if self.regexp is not None else r"\w[\w']+"
        words = re.findall(regexp, line, 0)
        return words

    def __test_for_text(self):
        """
        Utility method to validate a text file is being processed.
        :return: True if text is found at the beginning of the file.  Otherwise, False is returned.
        """
        chr_cnt = 0
        bin_cnt = 0
        with open(self.filename, 'r') as f:
            for line in f:
                bc = self.__find_binary(line)
                chr_cnt += len(line)
                bin_cnt += bc
        return False if bin_cnt/chr_cnt > 0.30 else True

    def __find_binary(self, line):
        """
        Utility method to validate a line of text contains binary characters or not.
        :param line: A string containing the characters from the line of the text file.
        :return: The number of binary characters found in the string.
        """
        def isascii(s): return len(s) == len(s.encode())
        bc = 0
        if isascii(line):
            for c in line:
                if ord(c) < ord(' '):
                    bc += 1
                elif ord(c) > 126:
                    bc += 1
        else:
            bc += len(line)
        return bc

