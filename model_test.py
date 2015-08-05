import unittest
from model import Submit, Run, Problem


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
        self.submit = Submit('0', ('1', '1'), '179', '0', self.runs, '1', 'kirov')
        self.assertEqual(self.submit.problem_id[1], '1')
        self.assertEqual(self.submit.problem_id[0], '1')
        self.assertEqual(self.submit.submit_id, '0')
        self.assertEqual(self.submit.runs, self.runs)
        self.assertEqual(self.submit.user_id, '179')
        self.assertEqual(self.submit.lang_id, '0')
        self.assertEqual(self.submit.outcome, '1')
        self.assertEqual(self.submit.scoring, 'kirov')

    def test_str_runs(self):
        self.submit = Submit('0', ('1', '1'), '179', '0', self.runs, '1', 'kirov')
        self.assertEqual(str(self.submit), "Submit: 0; Result: 1; User id: 179; Runs: Case #0 Outcome 1, "
                                           "Case #1 Outcome 1.")

    def test_results_of_runs(self):
        self.submit = Submit('0', ('1', '1'), '179', '0', self.runs, '1', 'kirov')
        self.assertEqual(self.submit.runs_results, self.runs_results)


class TestProblem(unittest.TestCase):

    def setUp(self):
        self.prob = Problem(("1", "17"), "Testname", ["1", "2", "3"])

    def test_init(self):
        self.assertEqual(self.prob.problem_id, ("1", "17"))
        self.assertEqual(self.prob.name, "Testname")
        self.assertEqual(self.prob.cases, ["1", "2", "3"])

    def test_str(self):
        self.assertEqual(str(self.prob), 'Problem #17 ("Testname") from contest #1')


if __name__ == "__main__":
    unittest.main()
