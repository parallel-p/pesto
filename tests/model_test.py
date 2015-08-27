import unittest

from model import Submit, Run, Problem, User, Contest


class TestRun(unittest.TestCase):
    def setUp(self):
        self.run = Run(None, '1', '2', '1', '100', 'OK')

    def test_init(self):
        self.assertEqual(self.run.problem_id, None)
        self.assertEqual(self.run.submit_id, '1')
        self.assertEqual(self.run.case_id, '2')
        self.assertEqual(self.run.real_time, '1')
        self.assertEqual(self.run.time, '100')
        self.assertEqual(self.run.outcome, 'OK')


    def test_str(self):
        self.assertEqual(str(self.run), "Case #2 Outcome OK")

    def test_repr(self):
        self.assertEqual(str(self.run), repr(self.run))


class TestSubmit(unittest.TestCase):
    def setUp(self):
        self.runs = []
        self.runs_results = []

        for i in range(2):
            self.runs_results.append('1')
            self.runs.append(Run('0', '0', str(i), '1', '100', '1'))

        self.runs_results = ''.join(self.runs_results)

    def test_init(self):
        self.submit = Submit('0', ('1', '1'), '179', '0', self.runs, '1', 'kirov', 37)
        self.assertEqual(self.submit.problem_id[1], '1')
        self.assertEqual(self.submit.problem_id[0], '1')
        self.assertEqual(self.submit.submit_id, '0')
        self.assertEqual(self.submit.runs, self.runs)
        self.assertEqual(self.submit.user_id, '179')
        self.assertEqual(self.submit.lang_id, '0')
        self.assertEqual(self.submit.outcome, '1')
        self.assertEqual(self.submit.scoring, 'kirov')
        self.assertEqual(self.submit.timestamp, 37)

    def test_str_runs(self):
        self.submit = Submit('0', ('1', '1'), '179', '0', self.runs, '1', 'kirov', 37)
        self.assertEqual(str(self.submit), "Submit: 0; Result: 1; User id: 179; Runs: Case #0 Outcome 1, "
                                           "Case #1 Outcome 1.")

    def test_results_of_runs(self):
        self.submit = Submit('0', ('1', '1'), '179', '0', self.runs, '1', 'kirov', 37)
        self.assertEqual(self.submit.runs_results, self.runs_results)


class TestProblem(unittest.TestCase):
    def setUp(self):
        self.prob = Problem(("1", "17"), '42', "Testname", ["1", "2", "3"])

    def test_init(self):
        self.assertEqual(self.prob.problem_id, ("1", "17"))
        self.assertEqual(self.prob.polygon_id, '42')
        self.assertEqual(self.prob.name, "Testname")
        self.assertEqual(self.prob.cases, ["1", "2", "3"])

    def test_str(self):
        self.assertEqual(str(self.prob), 'Problem #17 ("Testname") from contest #1')


class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User(1, 'lksh')

    def test_init(self):
        self.assertEqual(self.user.user_id, 1)
        self.assertEqual(self.user.origin, 'lksh')

    def test_str(self):
        self.assertEqual(str(self.user), 'User #1 from lksh')


class TestContest(unittest.TestCase):
    def setUp(self):
        self.contest = Contest('42', 'orig', 'Untitled', 'ACM')

    def test_init(self):
        self.assertEqual(self.contest.contest_id, '42')
        self.assertEqual(self.contest.origin, 'orig')
        self.assertEqual(self.contest.name, 'Untitled')
        self.assertEqual(self.contest.scoring, 'ACM')

    def test_str(self):
        self.assertEqual(str(self.contest), 'Contest Untitled (#42) from orig, scoring ACM')


if __name__ == "__main__":
    unittest.main()
