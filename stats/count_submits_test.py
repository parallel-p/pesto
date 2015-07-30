from stats.count_submits import count_submits
import unittest


class CountMethodTest(unittest.TestCase):
    def count_test(self):
        #CSV contains information only about interesting contest
        res = {"1":1, "2":1, "3":1}
        self.assertEqual(count_submits('../testdata/count_submit_test/000017', '../testdata/count_submit_test/useful_runs_count_submit_test.csv'), res)

        res = {}
        #CSV dasn't contains information about interesting contest
        self.assertEqual(count_submits('../testdata/count_submit_test/000017', '../testdata/count_submit_test/unuseful_runs_count_submit_test.csv'), res)

        res = {"1":1, "3":1}
        #CSV contains information not only about interesting contest
        self.assertEqual(count_submits('../testdata/count_submit_test/000017', '../testdata/count_submit_test/mixed_runs_count_submit_test.csv'), res)

    def without_csv(self):
        #CSV is empty
        res = dict()
        self.assertEqual(count_submits('../testdata/count_submit_test/000017', '../testdata/count_submit_test/empty_runs_count_submit_test.csv'), res)

        #without CSV
        res = dict()
        self.assertEqual(count_submits('../testdata/count_submit_test/000017_count_submit_test', None), res)

    def bad_base_path_test(self):
        with self.assertRaises(Exception):
           self.assertEqual(count_submits(''), [])
        with self.assertRaises(Exception):
            self.assertEqual(count_submits('', ''), [])

if __name__ == 'main':
    unittest.main()
