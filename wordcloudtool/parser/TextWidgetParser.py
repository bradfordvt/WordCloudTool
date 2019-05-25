"""
@package wordcloudtool.parser
@author Bradford G. Van Treuren
@copyright: Copyright (c) Bradford G. Van Treuren 2019. All rights reserved.
@version: 0.1
@change: Mar 26, 2019 - Initial release
Common class for text based widget decoders providing source for words to cloudify.
"""
from wordcloudtool.parser.ParserBase import ParserBase
import re


class TextWidgetParser(ParserBase):
    """
    Common features for all Text Widget parsing.
    """
    def __init__(self, text):
        """
        Constructor
        :param text: A reference of variable containing the text to be parsed.
                     This is typically the text variable for the widget.
                     Thus, changes to the widget would be reflected here.
        """
        super(ParserBase, self).__init__()
        self.regexp = None
        self.text = text

    def parse(self):
        """
        Parse the contents of the text field and extract all the words into a list.
        :return: A list of words from the text widget.
        """
        ret = []
        for line in self.text:
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
