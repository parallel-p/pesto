import unittest
import os.path
from stats.submits_over_test_cases_numbers import SubmitsOverTestCasesNumbers
from ejudge_parse import ejudge_parse


class SubmitsOverCasesTest(unittest.TestCase):
    def setUp(self):
        self.visitor = SubmitsOverTestCasesNumbers()
        self.base_path = os.path.join('testdata', 'submits_over_test_cases_numbers')
    
    def test_good(self):
        correct = {('1', '1'): {2: 1, 3: 2}, ('1', '2'): {3: 2}}
        ejudge_parse([os.path.join(self.base_path, '001')], os.path.join(self.base_path, 'db.csv'), self.visitor)
        self.assertEqual(self.visitor.get_stat_data(), correct)

    def test_bad_submit(self):
        with self.assertRaises(Exception):
            self.visitor.visit(None)

    def test_pretty(self):
        correct = "-------------\nProblem #('1', '1')\n-------------\n    2 ################################################## 1\n    3 #################################################################################################### 2\n-------------\nProblem #('1', '2')\n-------------\n    3 #################################################################################################### 2\n"
        ejudge_parse([os.path.join(self.base_path, '001')], os.path.join(self.base_path, 'db.csv'), self.visitor)
        self.assertEqual(self.visitor.pretty_print(), correct)