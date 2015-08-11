import unittest
from unittest.mock import Mock
from dao_cases import DAOCases

class DAOCasesTest(object):
    def test_load(self):
        row = ("1", "1", "1", "440fae04f9e3619de0b8e9319a6a5f4b")
        self.assertEqual(DAOCases.load(row), "440fae04f9e3619de0b8e9319a6a5f4b")


if __name__ == "__main__":
    unittest.main()
