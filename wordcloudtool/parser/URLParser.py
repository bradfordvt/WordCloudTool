"""
@package wordcloudtool.parser
@author Bradford G. Van Treuren
@copyright: Copyright (c) Bradford G. Van Treuren 2019. All rights reserved.
@version: 0.1
@change: Mar 26, 2019 - Initial release
Common class for url based text decoders providing source for words to cloudify.
"""
from wordcloudtool.parser.ParserBase import ParserBase
import re
import urllib3


class URLParser(ParserBase):
    """
    Common features for all URL parsing.
    """
    def __init__(self, url):
        """
        Constructor
        :param url: A string containing the URL of the site to be processed.
        """
        super(ParserBase, self).__init__()
        self.regexp = None
        self.text = None
        self.url = url

    def parse(self):
        """
        Parse the contents of the text data and extract all the words into a list.
        :return: A list of words from the text data.
        """
        http = urllib3.PoolManager()
        response = http.request('GET', self.url)
        self.text = response.data.decode('utf-8')
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
