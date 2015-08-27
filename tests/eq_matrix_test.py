import unittest

from stats.eq_matrix import EqMatrix
from model import Submit
from model import Run


class PositiveTests(unittest.TestCase):
    def setUp(self):
        self.matrix = EqMatrix()

    def test_allsame(self):
        runs = []
        for i in range(4):
            runs.append(Run(0, 0, i, '100', '100', "OK"))

        submits = []
        for i in range(10):
            submits.append(Submit(i, (0, 0), 0, 0, runs, 0, 'ACM', 37))

        for submit in submits:
            self.matrix.visit(submit)

        sample = ("\t" + "".join("{:>9}".format(elem) for elem in [10, 10, 10, 10]) + "\n" +
                  "0\t" + "".join("{:>9}".format(elem) for elem in [1, 2, 3, 4]) + "\n" +
                  "1\t" + "".join("{:>9}".format(str(elem) + "%") for elem in [0.0, 0.0, 0.0, 0.0]) + "\n" +
                  "2\t" + "".join("{:>9}".format(str(elem) + "%") for elem in [0.0, 0.0, 0.0, 0.0]) + "\n" +
                  "3\t" + "".join("{:>9}".format(str(elem) + "%") for elem in [0.0, 0.0, 0.0, 0.0]) + "\n" +
                  "4\t" + "".join("{:>9}".format(str(elem) + "%") for elem in [0.0, 0.0, 0.0, 0.0]) + "\n")

        self.assertEqual(self.matrix.pretty_print(), sample)

    def test_mixed(self):
        runs = []
        runs.append(Run(0, 0, 0, '100', '100', "OK"))
        runs.append(Run(0, 0, 1, '100', '100', "WA"))
        runs.append(Run(0, 0, 2, '100', '100', "WA"))
        runs.append(Run(0, 0, 3, '100', '100', "WA"))

        submits = []
        for i in range(10):
            submits.append(Submit(i, (0, 0), 0, 0, runs, 0, 'ACM', 37))

        sample = ("\t" + "".join("{:>9}".format(elem) for elem in [10, 10, 10, 10]) + "\n" +
                  "0\t" + "".join("{:>9}".format(elem) for elem in [1, 2, 3, 4]) + "\n" +
                  "1\t" + "".join("{:>9}".format(str(elem) + "%") for elem in [0.0, 100.0, 100.0, 100.0]) + "\n" +
                  "2\t" + "".join("{:>9}".format(str(elem) + "%") for elem in [100.0, 0.0, 0.0, 0.0]) + "\n" +
                  "3\t" + "".join("{:>9}".format(str(elem) + "%") for elem in [100.0, 0.0, 0.0, 0.0]) + "\n" +
                  "4\t" + "".join("{:>9}".format(str(elem) + "%") for elem in [100.0, 0.0, 0.0, 0.0]) + "\n")

        for submit in submits:
            self.matrix.visit(submit)

        self.assertEqual(self.matrix.pretty_print(), sample)

    def test_different(self):
        runs = []
        runs.append(Run(0, 0, 0, '100', '100', "OK"))
        runs.append(Run(0, 0, 1, '100', '100', "WA"))
        runs.append(Run(0, 0, 2, '100', '100', "OK"))
        runs.append(Run(0, 0, 3, '100', '100', "WA"))

        submits = []
        for i in range(10):
            submits.append(Submit(i, (0, 0), 0, 0, runs, 0, 'ACM', 37))

        for submit in submits:
            self.matrix.visit(submit)

        sample = ("\t" + "".join("{:>9}".format(elem) for elem in [10, 10, 10, 10]) + "\n" +
                  "0\t" + "".join("{:>9}".format(elem) for elem in [1, 2, 3, 4]) + "\n" +
                  "1\t" + "".join("{:>9}".format(str(elem) + "%") for elem in [0.0, 100.0, 0.0, 100.0]) + "\n" +
                  "2\t" + "".join("{:>9}".format(str(elem) + "%") for elem in [100.0, 0.0, 100.0, 0.0]) + "\n" +
                  "3\t" + "".join("{:>9}".format(str(elem) + "%") for elem in [0.0, 100.0, 0.0, 100.0]) + "\n" +
                  "4\t" + "".join("{:>9}".format(str(elem) + "%") for elem in [100.0, 0.0, 100.0, 0.0]) + "\n")

        self.assertEqual(self.matrix.pretty_print(), sample)

    def test_zero_submits(self):
        self.assertEqual(self.matrix.pretty_print(), "No submits")

    def test_difruns(self):
        runs = []
        runs.append(Run(0, 0, 0, '100', '100', "OK"))
        runs.append(Run(0, 0, 1, '100', '100', "WA"))
        runs.append(Run(0, 0, 2, '100', '100', "OK"))
        runs.append(Run(0, 0, 3, '100', '100', "WA"))

        submits = []
        for i in range(4):
            submits.append(Submit(i, (0, 0), 0, 0, runs[:2], 0, 'ACM', 37))
            submits.append(Submit(i, (0, 0), 0, 0, runs, 0, 'ACM', 37))
        submits.append(Submit(i, (0, 0), 0, 0, runs[:1], 0, 'ACM', 37))
        submits.append(Submit(i, (0, 0), 0, 0, runs[:1], 0, 'ACM', 37))

        for submit in submits:
            self.matrix.visit(submit)

        sample = ("\t" + "".join("{:>9}".format(elem) for elem in [10, 8, 4, 4]) + "\n" +
                  "0\t" + "".join("{:>9}".format(elem) for elem in [1, 2, 3, 4]) + "\n" +
                  "1\t" + "".join("{:>9}".format(str(elem) + "%") for elem in [0.0, 100.0, 0.0, 100.0]) + "\n" +
                  "2\t" + "".join("{:>9}".format(str(elem) + "%") for elem in [100.0, 0.0, 100.0, 0.0]) + "\n" +
                  "3\t" + "".join("{:>9}".format(str(elem) + "%") for elem in [0.0, 100.0, 0.0, 100.0]) + "\n" +
                  "4\t" + "".join("{:>9}".format(str(elem) + "%") for elem in [100.0, 0.0, 100.0, 0.0]) + "\n")

        # sample = ("10 0 4 0\n" +
        # "0 8 0 4\n"  +
        #           "4 0 4 0\n"  +
        #           "0 4 0 4\n")

        self.assertEqual(self.matrix.pretty_print(), sample)

    def test_raw_data(self):
        runs = []
        runs.append(Run(0, 0, 0, '100', '100', "OK"))
        runs.append(Run(0, 0, 1, '100', '100', "WA"))
        runs.append(Run(0, 0, 2, '100', '100', "OK"))
        runs.append(Run(0, 0, 3, '100', '100', "WA"))

        submits = []
        for i in range(4):
            submits.append(Submit(i, (0, 0), 0, 0, runs[:2], 0, 'ACM', 37))
            submits.append(Submit(i, (0, 0), 0, 0, runs, 0, 'ACM', 37))
        submits.append(Submit(i, (0, 0), 0, 0, runs[:1], 0, 'ACM', 37))
        submits.append(Submit(i, (0, 0), 0, 0, runs[:1], 0, 'ACM', 37))

        for submit in submits:
            self.matrix.visit(submit)

        sample = [[10, 0, 4, 0],
                  [0, 8, 0, 4],
                  [4, 0, 4, 0],
                  [0, 4, 0, 4]]

        self.assertEqual(self.matrix.get_stat_data(), sample)


if __name__ == "__main__":
    unittest.main()
