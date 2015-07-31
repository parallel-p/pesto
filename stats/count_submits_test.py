from stats.count_submits import SubmitsCounter
from ejudge_parse import ejudge_parse
from os.path import join
import unittest


class CountMethodTest(unittest.TestCase):

    def setUp(self):
        self.base_path = join('testdata', 'count_submit_test', '000017')
        self.data_path = join('testdata', 'count_submit_test')
        self.submits_counter = SubmitsCounter()

    def test_count_with_full_information_abount_submits(self):
        # CSV contains information only about interesting contest, problems 1 through 3 in contest 17 contain one submit
        good_result = 'Problem #1: 1 submits.\nProblem #2: 1 submits.\nProblem #3: 1 submits.\n'
        ejudge_parse([self.base_path], join(self.data_path, 'useful_runs_count_submit_test.csv'), self.submits_counter)
        self.assertEqual(self.submits_counter.pretty_print(), good_result)

    def test_count_without_some_information_abount_submits(self):
        # lines of csv dont corresponds submit in base, no information about contest 17 in csv
        good_result = ''
        ejudge_parse([self.base_path], join(self.data_path, 'unuseful_runs_count_submit_test.csv'), self.submits_counter)
        self.assertEqual(self.submits_counter.pretty_print(), good_result)

    def test_count_without_full_information_abount_submits(self):
        good_result = 'Problem #1: 1 submits.\nProblem #3: 1 submits.\n'
        ejudge_parse([self.base_path], join(self.data_path, 'mixed_runs_count_submit_test.csv'), self.submits_counter)
        # not every line of csv corresponds submit in base, no information about problem 2 in contest 1 in base
        self.assertEqual(self.submits_counter.pretty_print(), good_result)

    def test_without_csv(self):
        # CSV is empty, result is empty string
        good_result = ''
        ejudge_parse([self.base_path], join(self.data_path, 'empty_runs_count_submit_test.csv'), self.submits_counter)
        self.assertEqual(self.submits_counter.pretty_print(), good_result)

    def test_bad_submit(self):
        with self.assertRaises(Exception):
            self.submits_counter.update_submit(None)

if __name__ == 'main':
    unittest.main()
