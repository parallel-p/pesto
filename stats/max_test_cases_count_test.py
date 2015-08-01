import unittest
from stats.max_test_cases_count import MaxTestCasesCount
from model import Submit
from model import Run
from os.path import join


class MaxTestCountTest(unittest.TestCase):
    def setUp(self):
        self.many_runs_OK = []
        self.mixed = []
        self.lit_runs_WA = []
        answer = ['OK', 'WA']

        for i in range(10):
            self.many_runs_OK.append(Run(None, '1', i, answer[0]))
        for i in range(11):
            self.mixed.append(Run(None, '3', i, answer[i % 2]))
        for i in range(5):
            self.lit_runs_WA.append(Run(None, '2', i, answer[1]))

        self.submit1 = Submit('1', ('1', '1'), '1', self.many_runs_OK, '0')
        self.submit2 = Submit('2', ('2', '1'), '1', self.lit_runs_WA, '1')
        self.submit3 = Submit('3', ('1', '1'), '1', self.mixed, '1')
        self.good_csv_file_name = join("testdata", "max_test_count_test", "good.csv")
        self.test_csv_file_name = join("testdata", "max_test_count_test", "test.csv")

    def test_dict_data(self):
        visitor = MaxTestCasesCount(self.test_csv_file_name)
        visitor.visit(self.submit1)
        visitor.visit(self.submit2)
        visitor.visit(self.submit3)
        res = visitor.get_stat_data()
        self.assertEqual(res[("1", "1")], 11)
        self.assertEqual(res[("2", "1")], 5)

    def test_bad_file(self):
        visitor = MaxTestCasesCount("123823.**@3&*&")
        with self.assertRaises(OSError):
            visitor.get_stat_data()

    def test_data_writing(self):
        visitor = MaxTestCasesCount(self.test_csv_file_name)
        visitor.visit(self.submit1)
        visitor.visit(self.submit2)
        visitor.visit(self.submit3)
        visitor.get_stat_data()

        good_csv = open(self.good_csv_file_name, "r").readlines()
        test_csv = open(self.test_csv_file_name, "r").readlines()

        self.assertEqual(len(good_csv), len(test_csv))
        for line in good_csv:
            self.assertTrue(line in test_csv)


if __name__ == "main":
    unittest.main()

