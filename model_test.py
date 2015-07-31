import unittest
from model import Problem
from model import Submit
from model import Run
from memory_database import MemoryDatabase
import os.path


class TestProblemMethods(unittest.TestCase):

    def test_init_white(self):
        temp = Problem(0, 0, [0, 0])
        self.assertTrue(temp.contest_id == 0 and temp.problem_id == 0 and temp.case_ids == [0, 0])

    def test_str_white(self):
        temp = Problem('luck', 'duck', [0, 0])
        self.assertEqual(str(temp), 'Contest #luck Problem #duck\nCases: [0, 0]')\

    def test_get_submits(self):
        database = MemoryDatabase(os.path.join('testdata', 'problem_test', '000017'),
                                  os.path.join('testdata', 'problem_test',
                                               'useful_runs_count_submit_test.csv'))
        temp = database.get_problem('17', '3')
        standard = list()
        for submit in database.submits:
            if submit.problem.problem_id == temp.problem_id:
                standard.append(submit)
        self.assertEqual([submit for submit in temp.get_submits(database)], standard)


class TestRun(unittest.TestCase):

    def setUp(self):
        self.run = Run(None, '1', '2', 'OK')

    def test_init(self):
        self.assertEqual(self.run.problem, None)
        self.assertEqual(self.run.submit_id, '1')
        self.assertEqual(self.run.case_id, '2')
        self.assertEqual(self.run.outcome, 'OK')

    def test_str(self):
        self.assertEqual(str(self.run), "Case #2 Outcome OK")


class PositiveTests(unittest.TestCase):

    def setUp(self):
        self.runs = []
        self.runs_results = []

        for i in range(2):
            self.runs_results.append(str(1))
            self.runs.append(Run(0, 0, i, 1))

        self.runs_results = ''.join(self.runs_results)

    def test_init(self):
        self.submit = Submit(0, 1, 179, self.runs, 1)
        self.assertEqual(self.submit.problem_id, 1)
        self.assertEqual(self.submit.submit_id, 0)
        self.assertEqual(self.submit.runs, self.runs)
        self.assertEqual(self.submit.user_id, 179)
        self.assertEqual(self.submit.outcome, 1)

    def test_str_runs(self):
        self.submit = Submit(0, 1, 179, self.runs, 1)
        self.assertEqual(str(self.submit), "Submit: 0; Result: 1; User id: 179; Runs: Case #0 Outcome 1, "
                                           "Case #1 Outcome 1.")

    def test_results_of_runs(self):
        self.submit = Submit(0, 1, 179, self.runs, 1)
        self.assertEqual(self.submit.runs_results, self.runs_results)


if __name__ == "__main__":
    unittest.main()