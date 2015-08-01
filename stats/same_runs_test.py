import unittest
from model import Submit
from model import Run
from stats.same_runs import SameRuns


class PositiveTests(unittest.TestCase):
    def setUp(self):
        self.same = SameRuns()

    def test_allsame(self):
        runs = []
        for i in range(4):
            runs.append(Run(0, 0, i, "OK"))

        submits = []
        for i in range(10):
            submits.append(Submit(i, (0, 0), 0, runs, 0))

        for submit in submits:
            self.same.visit(submit)

        # sample = ("10 10 10 10\n" +
        #           "10 10 10 10\n" +
        #           "10 10 10 10\n" +
        #           "10 10 10 10\n")

        self.assertEqual(self.same.pretty_print(), "0 1 2 3\n")

    def test_mixed(self):
        runs = []
        runs.append(Run(0, 0, 0, "OK"))
        runs.append(Run(0, 0, 1, "WA"))
        runs.append(Run(0, 0, 2, "WA"))
        runs.append(Run(0, 0, 3, "WA"))

        submits = []
        for i in range(10):
            submits.append(Submit(i, (0, 0), 0, runs, 0))

        # sample = ("10 0 0 0\n"   +
        #           "0 10 10 10\n" +
        #           "0 10 10 10\n" +
        #           "0 10 10 10\n")

        for submit in submits:
            self.same.visit(submit)

        self.assertEqual(self.same.pretty_print(), "1 2 3\n")

    def test_different(self):
        runs = []
        runs.append(Run(0, 0, 0, "OK"))
        runs.append(Run(0, 0, 1, "WA"))
        runs.append(Run(0, 0, 2, "OK"))
        runs.append(Run(0, 0, 3, "WA"))

        submits = []
        for i in range(10):
            submits.append(Submit(i, (0, 0), 0, runs, 0))

        for submit in submits:
            self.same.visit(submit)

        # sample = ("10 0 10 0\n" +
        #           "0 10 0 10\n" +
        #           "10 0 10 0\n" +
        #           "0 10 0 10\n")

        self.assertEqual(self.same.pretty_print(), "0 2\n1 3\n")

    def test_difruns(self):
        runs = []
        runs.append(Run(0, 0, 0, "OK"))
        runs.append(Run(0, 0, 1, "WA"))
        runs.append(Run(0, 0, 2, "OK"))
        runs.append(Run(0, 0, 3, "WA"))

        submits = []
        for i in range(4):
            submits.append(Submit(i, (0, 0), 0, runs[:2], 0))
            submits.append(Submit(i, (0, 0), 0, runs, 0))
        submits.append(Submit(i, (0, 0), 0, runs[:1], 0))
        submits.append(Submit(i, (0, 0), 0, runs[:1], 0))

        for submit in submits:
            self.same.visit(submit)

        # sample = ("10 0 4 0\n" +
        #           "0 8 0 4\n"  +
        #           "4 0 4 0\n"  +
        #           "0 4 0 4\n")

        self.assertEqual(self.same.pretty_print(), "")


if __name__ == "__main__":
    unittest.main()
