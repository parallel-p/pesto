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
        good = ('testdata\\ejudge_contest\\000001\\problems\\A\\tests\\001.dat'.replace('\\', os.path.sep),
                'testdata\\ejudge_contest\\000001\\problems\\A\\tests\\001.ans'.replace('\\', os.path.sep))
        self.assertEqual(contest.get_test_paths_by_problem_id(('1', '1')), good)

    def test_contest2(self):
        contest = EjudgeContest(os.path.join('testdata', 'ejudge_contest', '000002'))
        self.assertEqual(contest.get_contest_id(), '2')
        self.assertEqual(contest.get_problem_ids(), [('2', '1'), ('2', '2')])
        self.assertEqual(contest.get_short_name_by_problem_id(('2', '1')), 'A')
        good = ('testdata\\ejudge_contest\\000002\\tests\\A\\01'.replace('\\', os.path.sep),
                'testdata\\ejudge_contest\\000002\\tests\\A\\01.a'.replace('\\', os.path.sep))
        self.assertEqual(contest.get_test_paths_by_problem_id(('2', '1')), good)

if __name__ == "__main__":
    unittest.main()
