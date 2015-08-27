import unittest
from unittest.mock import Mock

from model import Submit, Run

from stats.same_runs import SameRunsKirov, SameRunsACM, SameRunsBigStat


class PositiveTestsKirov(unittest.TestCase):
    def setUp(self):
        self.same = SameRunsKirov()

    def test_allsame(self):
        runs = []
        for i in range(4):
            runs.append(Run(0, 0, i + 1, '100', '100', "OK"))

        submits = []
        for i in range(10):
            submits.append(Submit(i, (0, 0), 0, 0, runs, 0, 'ACM', 37))

        for submit in submits:
            self.same.visit(submit)

        # sample = ("10 10 10 10\n" +
        # "10 10 10 10\n" +
        #           "10 10 10 10\n" +
        #           "10 10 10 10\n")

        self.assertEqual(self.same.pretty_print(), 'Submits - 10\nEquivalent tests: {1 2 3 4}\n'
                                                   'we recommend removing: 3/4 (75%) {2 3 4}\nit will save: 3sec/4sec (75%)\n')

    def test_mixed(self):
        runs = []
        runs.append(Run(0, 0, 1, '100', '100', "OK"))
        runs.append(Run(0, 0, 2, '100', '100', "WA"))
        runs.append(Run(0, 0, 3, '100', '100', "WA"))
        runs.append(Run(0, 0, 4, '100', '100', "WA"))

        submits = []
        for i in range(10):
            submits.append(Submit(i, (0, 0), 0, 0, runs, 0, 'ACM', 37))

        # sample = ("10 0 0 0\n"   +
        # "0 10 10 10\n" +
        #           "0 10 10 10\n" +
        #           "0 10 10 10\n")

        for submit in submits:
            self.same.visit(submit)

        self.assertEqual(self.same.pretty_print(), 'Submits - 10\nEquivalent tests: {2 3 4}\nUnique tests: {1}\n'
                                                   'we recommend removing: 2/4 (50%) {3 4}\nit will save: 2sec/4sec (50%)\n')

    def test_different(self):
        runs = []
        runs.append(Run(0, 0, 1, '100', '100', "OK"))
        runs.append(Run(0, 0, 2, '100', '100', "WA"))
        runs.append(Run(0, 0, 3, '100', '100', "OK"))
        runs.append(Run(0, 0, 4, '100', '100', "WA"))

        submits = []
        for i in range(10):
            submits.append(Submit(i, (0, 0), 0, 0, runs, 0, 'ACM', 37))

        for submit in submits:
            self.same.visit(submit)

        # sample = ("10 0 10 0\n" +
        # "0 10 0 10\n" +
        #           "10 0 10 0\n" +
        #           "0 10 0 10\n")

        self.assertEqual(self.same.pretty_print(), 'Submits - 10\nEquivalent tests: {1 3} {2 4}\nwe recommend '
                                                   'removing: 2/4 (50%) {3 4}\nit will save: 2sec/4sec (50%)\n')

    def test_difruns(self):
        runs = []
        runs.append(Run(0, 0, 1, '100', '100', "OK"))
        runs.append(Run(0, 0, 2, '100', '100', "WA"))
        runs.append(Run(0, 0, 3, '100', '100', "OK"))
        runs.append(Run(0, 0, 4, '100', '100', "WA"))

        submits = []
        for i in range(4):
            submits.append(Submit(i, (0, 0), 0, 0, runs[:2], 0, 'ACM', 37))
            submits.append(Submit(i, (0, 0), 0, 0, runs, 0, 'ACM', 37))
        submits.append(Submit(i, (0, 0), 0, 0, runs[:1], 0, 'ACM', 37))
        submits.append(Submit(i, (0, 0), 0, 0, runs[:1], 0, 'ACM', 37))

        for submit in submits:
            self.same.visit(submit)

        # sample = ("10 0 4 0\n" +
        # "0 8 0 4\n"  +
        #           "4 0 4 0\n"  +
        #           "0 4 0 4\n")

        self.assertEqual(self.same.pretty_print(), 'Submits - 10\nUnique tests: {1 2}\n')


class TestsACM(unittest.TestCase):
    def setUp(self):
        self.same = SameRunsACM()

    def test_ACM_problem1(self):
        runs = []
        runs.append(Run(0, 0, 1, '100', '100', "OK"))
        runs.append(Run(0, 0, 2, '100', '100', "OK"))
        runs.append(Run(0, 0, 3, '100', '100', "OK"))

        runs1 = []
        runs1.append(Run(0, 0, 1, '100', '100', "OK"))
        runs1.append(Run(0, 0, 2, '100', '100', "OK"))
        runs1.append(Run(0, 0, 3, '100', '100', "WA"))

        self.same.visit(Submit(1, (0, 0), 0, 0, runs, 0, 'ACM', 37))
        self.same.visit(Submit(1, (0, 0), 0, 0, runs1, 0, 'ACM', 37))

        self.assertEqual(self.same.pretty_print(), 'Submits - 2\nEquivalent tests: {1 2}\nUnique tests: {3}\n'
                                                   'we recommend removing: 1/3 (33%) {2}\nit will save: 0sec/0sec (33%)\n')

    def test_ACM_problem2(self):
        runs = []
        runs.append(Run(0, 0, 1, '100', '100', "OK"))
        runs.append(Run(0, 0, 2, '100', '100', "OK"))
        runs.append(Run(0, 0, 3, '100', '100', "OK"))

        runs1 = []
        runs1.append(Run(0, 0, 1, '100', '100', "OK"))
        runs1.append(Run(0, 0, 2, '100', '100', "WA"))

        self.same.visit(Submit(1, (0, 0), 0, 0, runs, 0, 'ACM', 37))
        self.same.visit(Submit(1, (0, 0), 0, 0, runs1, 0, 'ACM', 37))

        self.assertEqual(self.same.pretty_print(), 'Submits - 2\nEquivalent tests: {2 3}\nUnique tests: {1}\n'
                                                   'we recommend removing: 1/3 (33%) {3}\nit will save: 0sec/0sec (20%)\n')

    def test_ACM_problem_hard(self):
        runs1 = []
        runs1.append(Run(0, 0, 2, '100', '100', "OK"))
        runs1.append(Run(0, 0, 1, '100', '100', "WA"))

        runs2 = []
        runs2.append(Run(0, 0, 2, '100', '100', "OK"))
        runs2.append(Run(0, 0, 1, '100', '100', "OK"))
        runs2.append(Run(0, 0, 3, '100', '100', "OK"))
        runs2.append(Run(0, 0, 4, '100', '100', "WA"))

        runs3 = []
        runs3.append(Run(0, 0, 2, '100', '100', "OK"))
        runs3.append(Run(0, 0, 1, '100', '100', "OK"))
        runs3.append(Run(0, 0, 3, '100', '100', "OK"))
        runs3.append(Run(0, 0, 4, '100', '100', "OK"))
        runs3.append(Run(0, 0, 5, '100', '100', "OK"))

        self.same.visit(Submit(1, (0, 0), 0, 0, runs1, 0, 'ACM', 37))
        self.same.visit(Submit(1, (0, 0), 0, 0, runs2, 0, 'ACM', 37))
        self.same.visit(Submit(1, (0, 0), 0, 0, runs3, 0, 'ACM', 37))

        self.assertEqual(self.same.pretty_print(), 'Submits - 3\nEquivalent tests: {1 3} {4 5}\nUnique tests: {2}\n'
                                                   'we recommend removing: 2/5 (40%) {3 5}\nit will save: 0sec/1sec (27%)\n')

    def test_ACM_problem_1(self):
        runs1 = []
        runs1.append(Run(0, 0, 1, '100', '100', "OK"))
        runs1.append(Run(0, 0, 2, '100', '100', "OK"))
        runs2 = []
        runs2.append(Run(0, 0, 1, '100', '100', "OK"))
        runs2.append(Run(0, 0, 2, '100', '100', "WA"))
        runs3 = []
        runs3.append(Run(0, 0, 1, '100', '100', "WA"))

        self.same.visit(Submit(1, (0, 0), 0, 0, runs1, 0, 'ACM', 37))
        self.same.visit(Submit(1, (0, 0), 0, 0, runs2, 0, 'ACM', 37))
        self.same.visit(Submit(1, (0, 0), 0, 0, runs3, 0, 'ACM', 37))

        self.assertEqual(self.same.pretty_print(), 'Submits - 3\nUnique tests: {1 2}\n')

    def test_ACM_(self):
        run1 = Mock()
        run1.case_id = 1
        run1.outcome = 'OK'
        run1.time = 3000

        run2 = Mock()
        run2.case_id = 2
        run2.outcome = 'OK'
        run2.time = 3500

        run3 = Mock()
        run3.case_id = 3
        run3.outcome = 'OK'
        run3.time = 2700

        submit = Mock()
        submit.runs = [run1, run2, run3]

        self.same.visit(submit)
        self.assertEqual(self.same.pretty_print(), 'Submits - 1\nEquivalent tests: {1 2 3}\n'
                                                   'we recommend removing: 2/3 (66%) {1 2}\nit will save: 6sec/9sec (70%)\n')


class TestingSameRunsFinalStats(unittest.TestCase):
    def setUp(self):
        self.srf = SameRunsBigStat()

    def test_this_shit(self):
        run1 = Mock()
        run1.case_id = 1
        run1.outcome = 'OK'
        run1.time = 3000

        run2 = Mock()
        run2.case_id = 2
        run2.outcome = 'OK'
        run2.time = 3500

        run3 = Mock()
        run3.case_id = 3
        run3.outcome = 'OK'
        run3.time = 2700

        submit = Mock()
        submit.runs = [run1, run2, run3]

        for i in range(10):
            submit.problem_id = i
            self.srf.visit(submit)
            self.srf.visit(submit)

        run4 = Mock()
        run4.case_id = 1
        run4.outcome = 'OK'
        run4.time = 3000

        run5 = Mock()
        run5.case_id = 2
        run5.outcome = 'WA'
        run5.time = 3000

        submit1 = Mock()
        submit1.runs = [run4, run5]
        self.srf.visit(submit1)

        self.assertEqual(self.srf.pretty_print(),
                         'WE RECOMMEND REMOVING: 20/32 (62%)\nIT WILL SAVE: 0D 0H 2M 10S / 0D 0H 3M 10S (68%)\n')


if __name__ == "__main__":
    unittest.main()
