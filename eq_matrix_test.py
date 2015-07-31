import unittest
from eq_matrix import get_eq_matrix
from model import Submit
from model import Problem
from model import Run


class PositiveTests(unittest.TestCase):
    def test_allsame(self):
        runs = []
        for i in range(4):
            runs.append(Run(0, 0, i, "OK"))
        
        problem = Problem(0, 0, [0, 1, 2, 3])
        submits = []
        for i in range(10):
            submits.append(Submit(i, problem, 0, runs, 0))

        sample = [[10] * 4 for i in range(4)]

        self.assertEqual(get_eq_matrix(submits), sample)

    def test_mixed(self):
        runs = []
        runs.append(Run(0, 0, 0, "OK"))
        runs.append(Run(0, 0, 1, "WA"))
        runs.append(Run(0, 0, 2, "WA"))
        runs.append(Run(0, 0, 3, "WA"))

        problem = Problem(0, 0, [0, 1, 2, 3])
        submits = []
        for i in range(10):
            submits.append(Submit(i, problem, 0, runs, 0))

        sample = [[10, 0, 0, 0], 
                  [0, 10, 10, 10],
                  [0, 10, 10, 10],
                  [0, 10, 10, 10]]

        self.assertEqual(get_eq_matrix(submits), sample)

    def test_different(self):
        runs = []
        runs.append(Run(0, 0, 0, "OK"))
        runs.append(Run(0, 0, 1, "WA"))
        runs.append(Run(0, 0, 2, "OK"))
        runs.append(Run(0, 0, 3, "WA"))

        problem = Problem(0, 0, [0, 1, 2, 3])
        submits = []
        for i in range(10):
            submits.append(Submit(i, problem, 0, runs, 0))

        sample = [[10, 0, 10, 0], 
                  [0, 10, 0, 10],
                  [10, 0, 10, 0],
                  [0, 10, 0, 10]]

        self.assertEqual(get_eq_matrix(submits), sample)

    def test_difruns(self):
        runs = []
        runs.append(Run(0, 0, 0, "OK"))
        runs.append(Run(0, 0, 1, "WA"))
        runs.append(Run(0, 0, 2, "OK"))
        runs.append(Run(0, 0, 3, "WA"))

        problem = Problem(0, 0, [0, 1, 2, 3])
        submits = []
        for i in range(4):
            submits.append(Submit(i, problem, 0, runs, 0))
            submits.append(Submit(i, problem, 0, runs[:2], 0))
        submits.append(Submit(i, problem, 0, runs[:1], 0))
        submits.append(Submit(i, problem, 0, runs[:1], 0))

        sample = [[10, 0, 4, 0], 
                  [0, 8, 0, 4],
                  [4, 0, 4, 0],
                  [0, 4, 0, 4]]

        self.assertEqual(get_eq_matrix(submits), sample)


if __name__ == "__main__":
    unittest.main() 