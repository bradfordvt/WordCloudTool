"""
@package wordcloudtool.parser
@author Bradford G. Van Treuren
@copyright: Copyright (c) Bradford G. Van Treuren 2019. All rights reserved.
@version: 0.1
@change: Apr 26, 2019 - Initial release
Specialized test class for ImageFileParser class.
"""
import unittest
import os
from wordcloudtool.parser.ImageFileParser import ImageFileParser


class MyTestCase(unittest.TestCase):
    png_file = 'TextImage1.png'  # PNG file name to use as test input file

    @classmethod
    def setUpClass(cls):
        """
        Create the input files the tests require for performing their tests.
        :return: Nothing...
        """
        cls.__createImageFile(cls.png_file)

    @classmethod
    def tearDownClass(cls):
        """
        Destroy the input files created for these tests.
        :return: Nothing...
        """
        cls.__destroyImageFile(cls.png_file)

    """
    Test Cases to test construction
    """
    def test_Constructor001(self):
        """
        Test that no value passed as filename triggers an AssertionError.
        :return:
        """
        try:
            tfp = ImageFileParser()
            self.assertFalse(True, 'No input did not trigger AssertionError.')
        except AssertionError as e:
            self.assertEqual(str(e), 'No filename was passed to the constructor.', 'Incorrect error message was detected.')
        except Exception:
            self.assertFalse(True, 'Wrong type of exeption was raised.')

    def test_Constructor002(self):
        """
        Test that filename is set properly in the underlying class and that it exists.
        :return:
        """
        try:
            tfp = ImageFileParser(self.png_file)
            self.assertEqual(tfp.filename, self.png_file, 'Filename was not set properly.')
        except Exception:
            self.assertFalse(True, 'Exception raised!.')

    def test_Constructor003(self):
        """
        Test that filename is detected as not existing and raises IOError.
        :return:
        """
        try:
            ImageFileParser('foo.png')
            self.assertFalse(True, 'Non-existent file did not trigger IOError.')
        except IOError as e:
            self.assertEqual(str(e), 'foo.png does not exist!', 'IOException not raised properly.')

    def test_Parse001(self):
        """
        Test that the parse method successfully parses the contents of the file.
        """
        golden = """Editfile
Preview
changes
hello
wortd
My
first
repository
on
GitHub
love
coffee
pizza
and
dancer
""".split()
        tfp = ImageFileParser(self.png_file)
        ret = tfp.parse()
        for i in range(0, len(golden)):
            self.assertEqual(golden[i], ret[i], 'Data mis-compare!')

    def test_Prune001(self):
        """
        Test that the prune method successfully prunes down the contents of words.
        """
        golden = """Editfile
Preview
changes
hello
first
repository
GitHub
love
coffee
pizza
dancer
""".split()
        tfp = ImageFileParser(self.png_file)
        words = tfp.parse()
        tfp.stopwords.add('wortd')
        words = tfp.prune(words)
        for i in range(0, len(golden)):
            self.assertEqual(golden[i], words[i], 'Data mis-compare!')

    @classmethod
    def __createImageFile(cls, filename):
        pass

    @classmethod
    def __destroyImageFile(cls, filename):
        pass


if __name__ == '__main__':
    unittest.main()
