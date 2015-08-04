import unittest
from stats.count_cases import CasesCounter
from model import Submit, Run


class TestCountCases(unittest.TestCase):
    def setUp(self):
        self.counter = CasesCounter()

    def test_common(self):
        self.counter.visit(Submit('1', (1, '1'), '0', '0', [Run('1', '-', 'OK', '0')] * 10, 'OK', 'ACM'))
        self.counter.visit(Submit('2', (1, '2'), '0', '0', [Run('2', '-', 'OK', '0')] * 20, 'OK', 'ACM'))
        self.counter.visit(Submit('3', (1, '3'), '0', '0', [Run('3', '-', 'OK', '0')] * 50, 'OK', 'ACM'))
        self.counter.visit(Submit('4', (1, '2'), '0', '0', [Run('4', '-', 'OK', '0')] * 30, 'OK', 'ACM'))
        self.assertEqual(self.counter.pretty_print(), 'Problem #1: 10 cases.\nProblem #2: 30 cases.\nProblem #3: 50 cases.\n')
        
    def test_empty(self):
        self.assertEqual(self.counter.pretty_print(), '')

    def test_bad_submit(self):
        with self.assertRaises(Exception):
            self.submits_counter.visit(None)

if __name__ == "__main__":
    unittest.main()
