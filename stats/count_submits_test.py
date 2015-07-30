from stats.count_submits import count_submits
from os.path import join
import unittest


class CountMethodTest(unittest.TestCase):

    def setUp(self):
        self.base_path = join('..', 'testdata', 'count_submit_test', '000017')
        self.data_path = join('..', 'testdata', 'count_submit_test')


    def test_count_with_full_information_abount_submits(self):
        #CSV contains information only about interesting contest, problems 1 through 3 in contest 17 contain one submit
        good_result = {"1": 1, "2": 1, "3": 1}
        self.assertEqual(count_submits(self.base_path, join(self.data_path, 'useful_runs_count_submit_test.csv')), good_result)

    def test_count_without_some_information_abount_submits(self):
        #lines of csv dont corresponds submit in base, no information about contest 17 in csv
        good_result = {}
        self.assertEqual(count_submits(self.base_path, join(self.data_path, 'unuseful_runs_count_submit_test.csv')), good_result)

    def test_count_without_full_information_abount_submits(self):
        good_result = {"1": 1, "3": 1}
        #not every line of csv corresponds submit in base, no information about problem 2 in contest 1 in base
        self.assertEqual(count_submits(self.base_path, join(self.data_path, 'mixed_runs_count_submit_test.csv')), good_result)

    def test_without_csv(self):
        #CSV is empty, result is empty dictionary
        good_result = dict()
        self.assertEqual(count_submits(self.base_path, join(self.data_path, 'empty_runs_count_submit_test.csv')), good_result)

    def test_bad_base_path(self):
        with self.assertRaises(Exception):
           self.assertEqual(count_submits(''), [])
        with self.assertRaises(Exception):
            self.assertEqual(count_submits('', ''), [])

if __name__ == 'main':
    unittest.main()
