import unittest
from stats.unique_set_tests_detector import UniqueSetTestsDetector
from ejudge_parse import ejudge_parse


class UniqueSetTestsTest(unittest.TestCase):
    def setUp(self):
        self.detector = UniqueSetTestsDetector()

    def test_common(self):
        ejudge_parse(['testdata/unique_set_test/1'], 'testdata/unique_set_test/common.csv', self.detector)
        res = self.detector.get_stat_data()
        self.assertEqual(res[('1', '1')]['OKOKOKOKOKOKOKOKOKOK'][1], 1)
        self.assertEqual(res[('1', '1')]['OKOKOKOKOK'][1], 2)
        self.assertEqual(res[('1', '1')]['OKOKOKOKWA'][1], 1)
        self.assertEqual(res[('1', '2')]['OKOKOKOKWA'][1], 2)

    def test_empty(self):
        ejudge_parse(['testdata/unique_set_test/2'], 'testdata/unique_set_test/common.csv', self.detector)
        res = self.detector.get_stat_data()
        self.assertEqual(res, {})

    def test_pretty_print(self):
        ejudge_parse(['testdata/unique_set_test/1'], 'testdata/unique_set_test/common.csv', self.detector)
        res = self.detector.pretty_print()
        good = '''***
contest_problem #1_1
  Run result:OK OK OK OK OK
   Submits count:2

  Run result:OK OK OK OK OK OK OK OK OK OK
   Submits count:1

  Run result:OK OK OK OK WA
   Submits count:1

***
contest_problem #1_2
  Run result:OK OK OK OK WA
   Submits count:2
'''
        self.assertEqual(res, good)

if __name__ == "__main__":
    unittest.main()
