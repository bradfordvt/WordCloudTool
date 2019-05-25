"""
@package wordcloudtool.parser
@author Bradford G. Van Treuren
@copyright: Copyright (c) Bradford G. Van Treuren 2019. All rights reserved.
@version: 0.1
@change: Apr 18, 2019 - Initial release
Specialized class for PDF text file based input decoders providing source for words to cloudify.
"""
from wordcloudtool.parser.FileParser import FileParser
import PyPDF2
import re


class PDFTextParser(FileParser):
    """
    Specialized class for PDF text file based input decoders.
    """
    def __init__(self, filename=None):
        """
        Constructor
        :param filename: Name of the PDF file to parse.
        """
        self.regexp = None
        super(PDFTextParser, self).__init__(filename)
        if not self.__test_for_pdf():
            raise IOError('{:s} is not a text based PDF file.'.format(filename))

    def parse(self):
        """
        Parse the contents of the PDF file and extract all the words into a list.
        :return: A list of words from the text file.
        """
        with open(self.filename, 'rb') as f:
            ret = []
            pdfReader = PyPDF2.PdfFileReader(f)
            num_pages = pdfReader.numPages
            count = 0
            line = ""
            while count < num_pages:
                pageObj = pdfReader.getPage(count)
                count += 1
                ret += self.__process_line(pageObj.extractText())
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

    def __test_for_pdf(self):
        """
        Utility method to validate a PDF text file is being processed.
        :return: True if text is found at the beginning of the file.  Otherwise, False is returned.
        """
        chr_cnt = 0
        bin_cnt = 0
        with open(self.filename, 'rb') as f:
            tag = f.read(4)
            if tag != b'%PDF':
                return False
            return True

