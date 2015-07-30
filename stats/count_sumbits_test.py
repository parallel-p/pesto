from stats.count_submits import count_submits
import unittest


class CountMethodTest(unittest.TestCase):
    def count_test(self):
        #CSV contains information only about interesting contest
        self.assertEqual(count_submits('../testdata/count_submit_test/000017', '../testdata/useful_runs_count_submit_test.csv'),
                         open('../testdata/good_result_1').read().rstrip())

        #CSV dasn't contains information about interesting contest
        self.assertEqual(count_submits('../testdata/count_submit_test/000017', '../testdata/unuseful_runs_count_submit_test.csv'),
                         open('../testdata/good_result_2').read().rstrip())

        #CSV contains information not only about interesting contest
        self.assertEqual(count_submits('../testdata/count_submit_test/000017', '../testdata/mixed_runs_count_submit_test.csv'),
                         open('../testdata/good_result_3').read().rstrip())
        #CSV is empty
        self.assertEqual(count_submits('../testdata/count_submit_test/000017', '../testdata/empty_runs_count_submit_test.csv'),
                         open('../testdata/good_result_4').read().rstrip())

        #without CSV
        self.assertEqual(count_submits('../testdata/count_submit_test/000017_count_submit_test'),
                         open('../testdata/good_result_4').read().rstrip())

    @unittest.skip("An exception is not intercepted")
    def bad_base_path_test(self):
        with self.assertRaises():
           self.assertEqual(count_submits(''), [])
        with self.assertRaises():
            self.assertEqual(count_submits('', ''), [])

if __name__ == 'main':
    unittest.main()
