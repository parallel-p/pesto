import unittest

from stats.max_test_cases_count import MaxTestCasesCount

from model import Submit
from model import Run


class MaxTestCountTest(unittest.TestCase):
    def setUp(self):
        self.many_runs_OK = []
        self.mixed = []
        self.lit_runs_WA = []
        answer = ['OK', 'WA']

        for i in range(10):
            self.many_runs_OK.append(Run(None, '1', i, '100', '100', answer[0]))
        for i in range(11):
            self.mixed.append(Run(None, '3', i, '100', '100', answer[i % 2]))
        for i in range(5):
            self.lit_runs_WA.append(Run(None, '2', i, '100', '100', answer[1]))

        self.submit1 = Submit('1', ('1', '1'), '1', '0', self.many_runs_OK, '0', 'ACM', 37)
        self.submit2 = Submit('2', ('2', '1'), '1', '0', self.lit_runs_WA, '1', 'ACM', 37)
        self.submit3 = Submit('3', ('1', '1'), '1', '0', self.mixed, '1', 'ACM', 37)

    def test_get_data(self):
        visitor1 = MaxTestCasesCount()
        visitor2 = MaxTestCasesCount()
        visitor1.visit(self.submit1)
        visitor1.visit(self.submit2)
        visitor2.visit(self.submit3)
        res1 = visitor1.get_stat_data()
        res2 = visitor2.get_stat_data()
        self.assertEqual(res1, 10)
        self.assertEqual(res2, 11)

    def test_pretty_print(self):
        visitor = MaxTestCasesCount()
        visitor.result = 42
        self.assertEqual(visitor.pretty_print(), 'Test cases:42')


if __name__ == "main":
    unittest.main()

