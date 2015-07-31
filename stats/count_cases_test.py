import unittest
from stats.count_cases import count_cases
from model import Problem


class TestCountCases(unittest.TestCase):
    def test_common(self):
        problems = {}
        problems[("42", "1")] = Problem("42", "1", [None] * 10)
        problems[("42", "2")] = Problem("42", "2", [None] * 15)
        problems[("43", "1")] = Problem("43", "1", [None] * 20)
        self.assertEqual(count_cases(problems, "42"), [('42', '1', 10), ('42', '2', 15)])
        self.assertEqual(count_cases(problems, "43"), [('43', '1', 20)])
        self.assertEqual(count_cases(problems, "azazaz"), [])

    def test_empty(self):
        problems = {}
        self.assertEqual(count_cases(problems, "42"), [])

    def test_no_case_ids(self):
        problems = {}
        problems[("42", "1")] = Problem("42", "1", None)
        with self.assertRaises(Exception):
            count_cases(problems, "42")

if __name__ == "__main__":
    unittest.main()
