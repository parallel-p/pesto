import unittest

import os.path
from ejudge_contest import EjudgeContest

class TestEjudgeContest(unittest.TestCase):

    def test_contest1(self):
        contest = EjudgeContest(os.path.join('testdata', 'ejudge_contest', '000001'))
        self.assertEqual(contest.dir_name, os.path.join('testdata', 'ejudge_contest', '000001'))
        self.assertEqual(contest.get_contest_id(), '1')
        self.assertEqual(contest.get_problem_ids(), [('1', '1'), ('1', '2')])
        self.assertEqual(contest.get_short_name_by_problem_id(('1', '1')), 'A')
        tests = contest.get_test_paths_by_problem_id(('1', '1'))
        self.assertEqual(len(tests), 5)
        good = ('testdata\\ejudge_contest\\000001\\problems\\A\\tests\\002.dat'.replace('\\', os.path.sep),
                'testdata\\ejudge_contest\\000001\\problems\\A\\tests\\002.ans'.replace('\\', os.path.sep))
        self.assertEqual(tests[1], good)

    def test_contest2(self):
        contest = EjudgeContest(os.path.join('testdata', 'ejudge_contest', '000002'))
        self.assertEqual(contest.get_contest_id(), '2')
        self.assertEqual(contest.get_problem_ids(), [('2', '1'), ('2', '2')])
        self.assertEqual(contest.get_short_name_by_problem_id(('2', '1')), 'A')
        tests = contest.get_test_paths_by_problem_id(('1', '1'))
        self.assertEqual(len(tests), 5)
        good = ('testdata\\ejudge_contest\\000002\\tests\\A\\02'.replace('\\', os.path.sep),
                'testdata\\ejudge_contest\\000002\\tests\\A\\02.a'.replace('\\', os.path.sep))
        self.assertEqual(tests[1], good)

    def test_no_cases(self):
        contest = EjudgeContest(os.path.join('testdata', 'ejudge_contest', '025950'))
        self.assertEqual(contest.get_contest_id(), '')
        self.assertEqual(len(contest.get_problem_ids()), 1)
        self.assertEqual(contest.get_short_name_by_problem_id(('', '1')), 'A')
        tests = contest.get_test_paths_by_problem_id(('1', '1'))
        self.assertFalse(tests)

if __name__ == "__main__":
    unittest.main()
