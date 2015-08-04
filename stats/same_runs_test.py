import unittest
from model import Submit
from model import Run
from stats.same_runs import SameRunsKirov


class PositiveTests(unittest.TestCase):
    def setUp(self):
        self.same = SameRunsKirov()

    def test_allsame(self):
        runs = []
        for i in range(4):
            runs.append(Run(0, 0, i + 1, "OK"))

        submits = []
        for i in range(10):
            submits.append(Submit(i, (0, 0), 0, 0, runs, 0, 'ACM'))

        for submit in submits:
            self.same.visit(submit)

        # sample = ("10 10 10 10\n" +
        #           "10 10 10 10\n" +
        #           "10 10 10 10\n" +
        #           "10 10 10 10\n")

        self.assertEqual(self.same.pretty_print(), 'Submits - 10\nEquivalent tests: {1 2 3 4}\n')

    def test_mixed(self):
        runs = []
        runs.append(Run(0, 0, 1, "OK"))
        runs.append(Run(0, 0, 2, "WA"))
        runs.append(Run(0, 0, 3, "WA"))
        runs.append(Run(0, 0, 4, "WA"))

        submits = []
        for i in range(10):
            submits.append(Submit(i, (0, 0), 0, 0, runs, 0, 'ACM'))

        # sample = ("10 0 0 0\n"   +
        #           "0 10 10 10\n" +
        #           "0 10 10 10\n" +
        #           "0 10 10 10\n")

        for submit in submits:
            self.same.visit(submit)

        self.assertEqual(self.same.pretty_print(), 'Submits - 10\nEquivalent tests: {2 3 4}\nUnique tests: {1}\n')

    def test_different(self):
        runs = []
        runs.append(Run(0, 0, 1, "OK"))
        runs.append(Run(0, 0, 2, "WA"))
        runs.append(Run(0, 0, 3, "OK"))
        runs.append(Run(0, 0, 4, "WA"))

        submits = []
        for i in range(10):
            submits.append(Submit(i, (0, 0), 0, 0, runs, 0, 'ACM'))

        for submit in submits:
            self.same.visit(submit)

        # sample = ("10 0 10 0\n" +
        #           "0 10 0 10\n" +
        #           "10 0 10 0\n" +
        #           "0 10 0 10\n")

        self.assertEqual(self.same.pretty_print(), 'Submits - 10\nEquivalent tests: {1 3} {2 4}\n')

    def test_difruns(self):
        runs = []
        runs.append(Run(0, 0, 1, "OK"))
        runs.append(Run(0, 0, 2, "WA"))
        runs.append(Run(0, 0, 3, "OK"))
        runs.append(Run(0, 0, 4, "WA"))

        submits = []
        for i in range(4):
            submits.append(Submit(i, (0, 0), 0, 0, runs[:2], 0, 'ACM'))
            submits.append(Submit(i, (0, 0), 0, 0, runs, 0, 'ACM'))
        submits.append(Submit(i, (0, 0), 0, 0, runs[:1], 0, 'ACM'))
        submits.append(Submit(i, (0, 0), 0, 0, runs[:1], 0, 'ACM'))

        for submit in submits:
            self.same.visit(submit)

        # sample = ("10 0 4 0\n" +
        #           "0 8 0 4\n"  +
        #           "4 0 4 0\n"  +
        #           "0 4 0 4\n")

        self.assertEqual(self.same.pretty_print(), 'Submits - 10\nUnique tests: {1 2}\n')

    # def test_hard(self):
        # runs1 = []
        # for i in range(4):
        #     runs1.append(Run(10, 10, i, "OK"))
        #
        # submits1 = []
        # for i in range(10):
        #     submits1.append(Submit(i, (10, 10), 10, 0, runs1, 10))
        #
        # for submit in submits1:
        #     self.same.visit(submit)
        #
        # # sample = ("10 10 10 10\n" +
        # #           "10 10 10 10\n" +
        # #           "10 10 10 10\n" +
        # #           "10 10 10 10\n")
        #
        # runs = []
        # runs.append(Run(0, 0, 0, "OK"))
        # runs.append(Run(0, 0, 1, "WA"))
        # runs.append(Run(0, 0, 2, "WA"))
        # runs.append(Run(0, 0, 3, "WA"))
        #
        # submits = []
        # for i in range(10):
        #     submits.append(Submit(i, (0, 0), 0, 0, runs, 0))
        #
        # # sample = ("10 0 0 0\n"   +
        # #           "0 10 10 10\n" +
        # #           "0 10 10 10\n" +
        # #           "0 10 10 10\n")
        #
        # for submit in submits:
        #     self.same.visit(submit)
        #
        # self.assertEqual(self.same.pretty_print(), "0 0:\n1 2 3\n10 10:\n0 1 2 3\n")


if __name__ == "__main__":
    unittest.main()
