from unittest.mock import Mock
import unittest

from stats.count_submits import SubmitsCounter


class CountMethodTest(unittest.TestCase):
    def setUp(self):
        self.submits_counter = SubmitsCounter()

    def test_empty(self):
        self.assertFalse(self.submits_counter.pretty_print())

    def test_visit(self):
        self.submits_counter.visit(Mock(problem_id=('1', '2')))
        self.submits_counter.visit(Mock(problem_id=('1', '1')))
        self.submits_counter.visit(Mock(problem_id=('1', '1')))
        res = self.submits_counter.pretty_print().strip()
        good = 'Problem #1: 2 submits.\nProblem #2: 1 submit.'
        self.assertEqual(res, good)

    def test_sort(self):
        self.submits_counter.visit(Mock(problem_id=('1', '2')))
        self.submits_counter.visit(Mock(problem_id=('1', '10')))
        res = self.submits_counter.pretty_print().strip()
        good = 'Problem #2: 1 submit.\nProblem #10: 1 submit.'
        self.assertEqual(res, good)

    def test_string_id(self):
        self.submits_counter.visit(Mock(problem_id=('1', '2')))
        self.submits_counter.visit(Mock(problem_id=('1', '10')))
        self.submits_counter.visit(Mock(problem_id=('1', 'a')))
        res = self.submits_counter.pretty_print().strip()
        good = 'Problem #10: 1 submit.\nProblem #2: 1 submit.\nProblem #a: 1 submit.'
        self.assertEqual(res, good)


if __name__ == 'main':
    unittest.main()
