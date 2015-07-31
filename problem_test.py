import unittest
from model import Problem
from memory_database import MemoryDatabase
import os.path
import sys

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
        self.assertEqual(temp.get_submits(database), standard)
if __name__ == '__main__':
    unittest.main()

