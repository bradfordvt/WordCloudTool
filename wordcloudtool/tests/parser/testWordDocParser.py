"""
@package wordcloudtool.parser
@author Bradford G. Van Treuren
@copyright: Copyright (c) Bradford G. Van Treuren 2019. All rights reserved.
@version: 0.1
@change: Apr 26, 2019 - Initial release
Specialized test class for WordDocParser class.
"""
import unittest
from wordcloudtool.parser.WordDocParser import WordDocParser


class MyTestCase(unittest.TestCase):
    png_file = 'TestFile1.docx'  # DOCX file name to use as test input file

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
            tfp = WordDocParser()
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
            tfp = WordDocParser(self.png_file)
            self.assertEqual(tfp.filename, self.png_file, 'Filename was not set properly.')
        except Exception:
            self.assertFalse(True, 'Exception raised!.')

    def test_Constructor003(self):
        """
        Test that filename is detected as not existing and raises IOError.
        :return:
        """
        try:
            WordDocParser('foo.png')
            self.assertFalse(True, 'Non-existent file did not trigger IOError.')
        except IOError as e:
            self.assertEqual(str(e), 'foo.png does not exist!', 'IOException not raised properly.')

    def test_Parse001(self):
        """
        Test that the parse method successfully parses the contents of the file.
        """
        golden = """Responsibilities
Research
and
develop
BI
models
and
data
analysis
Collaborate
with
Network
Engineering
Service
Assurance
Field
Operations
teams
to
understand
the
problem
and
devise
possible
solution
Keep
up
to
date
with
latest
technology
trends
Communicate
results
and
ideas
to
key
decision
makers
Implement
new
statistical
or
other
mathematical
methodologies
as
needed
for
specific
models
or
analysis
Optimize
joint
development
efforts
through
appropriate
database
use
and
project
design
Top
requirements
Experience
in
SQL
Modeling
Python
Any
ETL
tool
Experience
in
databases
like
Oracle
Postgres
PostGIS
SQL
queries
analysis
and
scripting
Experience
in
BI
Tools
like
Tableau
OBIEE
etc
Required
Skills
Experience
in
Statistical
modeling
Programming
in
Python
SQL
Database
technologies
Oracle
Postgres
SQL
Tableau
Analyzing
large
volume
of
data
Desired
Skills
PLSQL
ETL
Tools
BI
Tools
Tableau
Hadoop
platform
""".split()
        tfp = WordDocParser(self.png_file)
        ret = tfp.parse()
        for i in range(0, len(golden)):
            self.assertEqual(golden[i], ret[i], 'Data mis-compare!')

    def test_Prune001(self):
        """
        Test that the prune method successfully prunes down the contents of words.
        """
        golden = """Responsibilities
Research
develop
BI
models
data
analysis
Collaborate
Network
Engineering
Service
Assurance
Field
Operations
teams
understand
problem
devise
possible
solution
Keep
date
latest
technology
trends
Communicate
results
ideas
key
decision
makers
Implement
new
statistical
mathematical
methodologies
needed
specific
models
analysis
Optimize
joint
development
efforts
appropriate
database
use
project
design
Top
requirements
Experience
SQL
Modeling
Python
ETL
tool
Experience
databases
Oracle
Postgres
PostGIS
SQL
queries
analysis
scripting
Experience
BI
Tools
Tableau
OBIEE
etc
Required
Skills
Experience
Statistical
modeling
Programming
Python
SQL
Database
technologies
Oracle
Postgres
SQL
Tableau
Analyzing
large
volume
data
Desired
Skills
PLSQL
ETL
Tools
BI
Tools
Tableau
Hadoop
platform
""".split()
        tfp = WordDocParser(self.png_file)
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
