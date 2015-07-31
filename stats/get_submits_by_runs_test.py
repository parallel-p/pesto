import unittest
from stats.get_submits_by_runs import get_submits_by_runs
from model import Submit
from model import Run


class SubmitsByRunsTest(unittest.TestCase):
    def test_eq_good(self):
        submits = []
        for i in range(5):
            submits.append(Submit(i, i, i, [Run('17', 0, 0, 0, 0)] * 1, 'OK'))
        submits.append(Submit(i, i, i, [Run('17', 0, 0, 0, 0)] * 2, 'OK'))
        self.assertEqual(len(get_submits_by_runs(submits, 1, 'eq')), 5)
        self.assertEqual(len(get_submits_by_runs(submits, 1)), 5)

    def test_gt_good(self):
        submits = []
        for i in range(5):
            submits.append(Submit(i, i, i, [Run('17', 0, 0, 0, 0)] * i, 'OK'))
        self.assertEqual(len(get_submits_by_runs(submits, 3, 'gt')), 1)

    def test_lt_good(self):
        submits = []
        for i in range(5):
            submits.append(Submit(i, i, i, [Run('17', 0, 0, 0, 0)] * i, 'OK'))
        self.assertEqual(len(get_submits_by_runs(submits, 3, 'lt')), 3)    

    def test_bad_mode(self):
        with self.assertRaises(ValueError):
            get_submits_by_runs([], 3, 'qw')
        with self.assertRaises(ValueError):
            get_submits_by_runs([], 3, None)

    def test_bad_runs_count(self):
        with self.assertRaises(ValueError):
            get_submits_by_runs([], None)

    def test_bad_submits(self):
        with self.assertRaises(TypeError):
            get_submits_by_runs(None, 3)
        with self.assertRaises(TypeError):
            get_submits_by_runs([None], 3)
