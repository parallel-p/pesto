import unittest

from cases_stats import CasesStats


class TestCasesStats(unittest.TestCase):
    def setUp(self):
        self.stats = CasesStats([1, 2])

    def test_init(self):
        self.assertEqual(self.stats.result, None)
        self.assertEqual(self.stats.problems, [1, 2])
        self.assertEqual(str(self.stats), '')

    def test_stat_data(self):
        self.stats.result = 42
        self.assertEqual(self.stats.get_stat_data(), 42)


if __name__ == "__main__":
    unittest.main()
