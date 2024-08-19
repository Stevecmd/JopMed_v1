#!/usr/bin/python3
"""
Contains the class TestConsoleDocs
"""

import os
import sys
import console
import inspect
import pycodestyle
import unittest
import warnings
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)
warnings.filterwarnings("ignore", category=FutureWarning, module='pep8')

JOPMEDCommand = console.JOPMEDCommand


class TestConsoleDocs(unittest.TestCase):
    """Class for testing documentation of the console"""
    def test_pycodestyle_conformance_console(self):
        """Test that console.py conforms to pycodestyle."""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['console.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pycodestyle_conformance_test_console(self):
        """Test that tests/test_console.py conforms to pycodestyle."""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['tests/test_console.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_console_module_docstring(self):
        """Test for the console.py module docstring"""
        self.assertIsNot(console.__doc__, None,
                         "console.py needs a docstring")
        self.assertTrue(len(console.__doc__) >= 1,
                        "console.py needs a docstring")

    def test_JOPMEDCommand_class_docstring(self):
        """Test for the JOPMEDCommand class docstring"""
        self.assertIsNot(JOPMEDCommand.__doc__, None,
                         "JOPMEDCommand class needs a docstring")
        self.assertTrue(len(JOPMEDCommand.__doc__) >= 1,
                        "JOPMEDCommand class needs a docstring")
