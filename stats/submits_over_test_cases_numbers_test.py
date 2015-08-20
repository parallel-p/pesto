from unittest.mock import Mock
import unittest
import os.path
from stats.submits_over_test_cases_numbers import SubmitsOverTestCasesNumbers


class SubmitsOverCasesTest(unittest.TestCase):
    def setUp(self):
        self.visitor = SubmitsOverTestCasesNumbers()

    def test_init(self):
        self.assertFalse(self.visitor.get_stat_data())
        self.assertFalse(self.visitor.pretty_print())

    def test_visit(self):
        self.visitor.visit(Mock(problem_id=('1', '2'), runs = [0] * 5))
        self.visitor.visit(Mock(problem_id=('2', '1'), runs = [0] * 15))
        self.visitor.visit(Mock(problem_id=('1', '1'), runs = [0] * 5))
        self.visitor.visit(Mock(problem_id=('1', '1'), runs = [0] * 5))
        self.visitor.visit(Mock(problem_id=('1', '1'), runs = [0] * 10))
        self.assertEqual(self.visitor.get_stat_data(), {('2','1'): {15:1}, ('1','1'): {10:1, 5:2}, ('1','2'): {5:1}})
        res = self.visitor.pretty_print().strip().splitlines()
        good = ["-------------",
                "Problem #('1', '1')",
                "-------------",
                "   10 ################################################## 1",
                "    5 #################################################################################################### 2",
                "-------------",
                "Problem #('1', '2')",
                "-------------",
                "    5 #################################################################################################### 1",
                "-------------",
                "Problem #('2', '1')",
                "-------------",
                "   15 #################################################################################################### 1"]
        self.assertEqual(res, good)



if __name__ == "__main__":
    unittest.main()
