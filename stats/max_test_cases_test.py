import unittest
from stats.max_test_cases import max_test_cases
import os.path


class MaxTestCases(unittest.TestCase):
    def test_max_test_cases_test(self):
        filename = os.path.join('testdata', 'max_test_cases', 'max_test_cases.csv')
        self.assertEqual(max_test_cases(filename), {('17', '1'): 1,
                                                    ('17', '2'): 2,
                                                    ('17', '3'): 3,
                                                    ('17', '4'): 4})

