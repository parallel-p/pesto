import unittest
from unittest.mock import Mock
from dao_cases import DAOCases

class DAOCasesTest(unittest.TestCase):
    def test_load(self):
        row = {"id": "1", "case_id": "1", "problem_ref": "1", "io_hash": "440fae04f9e3619de0b8e9319a6a5f4b"}
        dao_cases = DAOCases(None)
        self.assertEqual(dao_cases.deep_load(row), "440fae04f9e3619de0b8e9319a6a5f4b")
        self.assertEqual(DAOCases.load(row), "440fae04f9e3619de0b8e9319a6a5f4b")


if __name__ == "__main__":
    unittest.main()
