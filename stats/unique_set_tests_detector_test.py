import unittest
from stats.unique_set_tests_detector import UniqueSetTestsDetector
from ejudge_parse import ejudge_parse


class UniqueSetTestsTest(unittest.TestCase):
    def setUp(self):
        self.detector = UniqueSetTestsDetector()

    def test_common(self):
        ejudge_parse(['testdata/unique_set_test/1'], 'testdata/unique_set_test/common.csv', self.detector)
        res = self.detector.get_stat_data()
        self.assertEqual(res['1_1']['OKOKOKOKOKOKOKOKOKOK'][1], 1)
        self.assertEqual(res['1_1']['OKOKOKOKOK'][1], 2)
        self.assertEqual(res['1_1']['OKOKOKOKWA'][1], 1)
        self.assertEqual(res['1_2']['OKOKOKOKWA'][1], 2)

    def test_empty(self):
        ejudge_parse(['testdata/unique_set_test/2'], 'testdata/unique_set_test/common.csv', self.detector)
        res = self.detector.get_stat_data()
        self.assertEqual(res, {})

if __name__ == "__main__":
    unittest.main()
