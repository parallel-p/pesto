import unittest
from stats.unique_test_sets_detector import get_uniq_test_results


class UniqueSetTestsTest(unittest.TestCase):
    @unittest.skip #We don't use MemoryDatabase anymore
    def test_common(self):
        res = get_uniq_test_results('testdata/unique_set_test/1', 'testdata/unique_set_test/common.csv')
        for i in res:
            i.sort(key=str)
        res.sort(key=str)
        self.assertEqual('OK OK OK OK OK OK OK OK OK OK', ' '.join([el.outcome for el in res[0][0][0]]))
        self.assertEqual(1, res[0][0][1])
        self.assertEqual('OK OK OK OK OK', ' '.join([el.outcome for el in res[0][1][0]]))
        self.assertEqual(2, res[0][1][1])
        self.assertEqual('OK OK OK OK WA', ' '.join([el.outcome for el in res[0][2][0]]))
        self.assertEqual(1, res[0][2][1])
        self.assertEqual('OK OK OK OK WA', ' '.join([el.outcome for el in res[1][0][0]]))
        self.assertEqual(2, res[1][0][1])

    @unittest.skip #We don't use MemoryDatabase anymore
    def test_empty(self):
        res = get_uniq_test_results('testdata/unique_set_test/2', 'testdata/unique_set_test/common.csv')
        self.assertEqual(res, [])

    @unittest.skip #We don't use MemoryDatabase anymore
    def test_not_all_submits(self):
        res = get_uniq_test_results('testdata/unique_set_test/1', 'testdata/unique_set_test/not_all_submits.csv')
        self.assertEqual('OK OK OK OK OK', ' '.join([el.outcome for el in res[0][0][0]]))
        self.assertEqual(1, res[0][0][1])

if __name__ == "__main__":
    unittest.main()
