"""
@package wordcloudtool.parser
@author Bradford G. Van Treuren
@copyright: Copyright (c) Bradford G. Van Treuren 2019. All rights reserved.
@version: 0.1
@change: Apr 18, 2019 - Initial release
Specialized test class for PDFImageParser class.
"""
import unittest
import os
from wordcloudtool.parser.PDFImageParser import PDFImageParser


class MyTestCase(unittest.TestCase):
    text_file = 'text_file.txt'  # Text file name to use as test input file
    pdf_file = 'pdf_file.pdf'  # PDF file name to use as test input file

    @classmethod
    def setUpClass(cls):
        """
        Create the input files the tests require for performing their tests.
        :return: Nothing...
        """
        cls.__createPDFFile(cls.pdf_file)

    @classmethod
    def tearDownClass(cls):
        """
        Destroy the input files created for these tests.
        :return: Nothing...
        """
        cls.__destroyPDFFile(cls.pdf_file)

    """
    Test Cases to test construction
    """
    def test_Constructor001(self):
        """
        Test that no value passed as filename triggers an AssertionError.
        :return:
        """
        try:
            tfp = PDFImageParser()
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
            tfp = PDFImageParser(self.pdf_file)
            self.assertEqual(tfp.filename, self.pdf_file, 'Filename was not set properly.')
        except Exception:
            self.assertFalse(True, 'Exception raised!.')

    def test_Constructor003(self):
        """
        Test that filename is detected as not existing and raises IOError.
        :return:
        """
        try:
            PDFImageParser('foo.pdf')
            self.assertFalse(True, 'Non-existent file did not trigger IOError.')
        except IOError as e:
            self.assertEqual(str(e), 'foo.pdf does not exist!', 'IOException not raised properly.')

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
UBwW
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
        tfp = PDFImageParser(self.pdf_file)
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
        tfp = PDFImageParser(self.pdf_file)
        words = tfp.parse()
        tfp.stopwords.add('UBwW')
        words = tfp.prune(words)
        for i in range(0, len(golden)):
            self.assertEqual(golden[i], words[i], 'Data mis-compare!')

    @classmethod
    def is_tool(cls, name):
        """Check whether `name` is on PATH and marked as executable."""

        # from whichcraft import which
        from shutil import which

        return which(name) is not None

    @classmethod
    def __createTextFile(cls, filename):
        """
        Create the contents of a text file to be used for the tests.
        :param filename: Filename of the text file to create.
        :return:
        """
        content = """Responsibilities:

Research and develop BI models and data analysis
Collaborate with Network Engineering, Service Assurance, Field Operations
teams to understand the problem and devise possible solution
Keep up-to-date with latest technology trends
Communicate results and ideas to key decision makers
Implement new statistical or other mathematical methodologies as needed for
specific models or analysis
Optimize joint development efforts through appropriate database use and
project design
Top 3 requirements:
1) Experience in SQL, Modeling, Python, Any ETL tool
2) Experience in databases like Oracle, Postgres, PostGIS, SQL queries
   analysis and scripting
3) Experience in BI Tools like Tableau, OBIEE etc.,

Required Skills:
1) Experience in Statistical modeling
2) Programming in Python, SQL
3) Database technologies - Oracle, Postgres, SQL
4) Tableau
5) Analyzing large volume of data

Desired Skills:
1) PLSQL, ETL Tools
2) BI Tools - Tableau
3) Hadoop platform
"""
        print('Creating {:s}.'.format(filename))
        fd = open(filename, 'w')
        fd.write(content)
        fd.close()

    @classmethod
    def __destroyTextFile(cls, filename):
        print('Destroying {:s}.'.format(filename))
        os.remove(os.path.abspath(filename))

    @classmethod
    def __createPDFFile(cls, filename):
        cls.__createTextFile(cls.text_file)
        if cls.is_tool("cupsfilter"):
            print("Using cupsfilter to create PDF.")
            os.system("".join(["cupsfilter", " ", cls.text_file, " > ", filename]))
        elif cls.is_tool("enscript") and cls.is_tool("ps2pdf"):
            print("Using enscript to create PDF.")
            os.system("".join(["enscript", " ", cls.text_file, " -B -o - | ps2pdf - ", filename]))
        elif cls.is_tool("unoconv"):
            print("Using unoconv to create PDF.")
            os.system("".join(["unoconv", " -f pdf ", cls.text_file]))
        else:
            raise AssertionError("No application available to create PDF file.")

    @classmethod
    def __destroyPDFFile(cls, filename):
        cls.__destroyTextFile(cls.text_file)
        print('Destroying {:s}.'.format(filename))
        os.remove(os.path.abspath(filename))


if __name__ == '__main__':
    unittest.main()
