"""
@package wordcloudtool.parser
@author Bradford G. Van Treuren
@copyright: Copyright (c) Bradford G. Van Treuren 2019. All rights reserved.
@version: 0.1
@change: Apr 26, 2019 - Initial release
Specialized class for word doc file based input decoders providing source for words to cloudify.
"""
from wordcloudtool.parser.FileParser import FileParser
import re
import textract


class WordDocParser(FileParser):
    """
    Specialized class for word document file based input decoders.
    """
    def __init__(self, filename=None):
        """
        Constructor
        :param filename: Name of the text file to parse.
        """
        self.regexp = None
        super(WordDocParser, self).__init__(filename)

    def parse(self):
        """
        Parse the contents of the word doc file and extract all the words into a list.
        :return: A list of words from the text file.
        """
        line = textract.process(self.filename, method='tesseract', language='eng')
        line = line.decode('ascii', 'ignore')
        ret = self.__process_line(line)
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
