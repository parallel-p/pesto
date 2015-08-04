import unittest
from unittest.mock import Mock
from case_counter import CaseCounter


class TestCaseCounter(unittest.TestCase):
    def setUp(self):
        problems = []
        problems.append(Mock(problem_id=('17', '1'), cases=[None] * 15))
        problems.append(Mock(problem_id=('17', '2'), cases=[None] * 10))
        problems.append(Mock(problem_id=('17', '3'), cases=[None] * 15))
        self.counter = CaseCounter(problems)

    def test_init(self):
        good = {('17', '1'): 15, ('17', '2'): 10, ('17', '3'): 15}
        self.assertEqual(self.counter.cases_count, good)

    def test_get_number(self):
        self.assertEqual(self.counter.get_cases_number(('17', '1')), 15)
        self.assertEqual(self.counter.get_cases_number(('17', '2')), 10)

    def test_missing_problem(self):
        self.assertEqual(self.counter.get_cases_number(('17', '42')), None)
        self.assertEqual(self.counter.get_cases_number('not_a_problem'), None)

if __name__ == "__main__":
    unittest.main()
