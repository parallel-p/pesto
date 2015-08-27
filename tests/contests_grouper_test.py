import unittest

from pesto_testcase import PestoTestCase
from model import Contest
from stats.contests_grouper import ContestsGrouper


class ProblemsGrouperTest(PestoTestCase):
    def setUp(self):
        contests = [Contest('123456', 'lksh', 'ЛКШ.2013.Зима.  A\'.День 3', 'ACM'),
                    Contest('789012', 'lksh', 'ЛКШ .Олимпиада.День3', 'Kirov'),
                    Contest('345678', 'lksh', 'ЛКШ.2011 . Июль', 'ACM'),
                    Contest('666666', 'hell', 'Левый контест', 'Kirov'),
                    Contest('666666', 'hell', None, 'ACM'),
                    Contest('127001', 'lksh', 'ЛКШ.Template', 'ACM')]
        self.grouper = ContestsGrouper(contests)

    def test_get_all(self):
        self.assertEqual(len(self.grouper.get_all_known_contests()), 3)
        self.assertTrue('123456' in self.grouper.get_all_known_contests())
        self.assertTrue('789012' in self.grouper.get_all_known_contests())
        self.assertTrue('345678' in self.grouper.get_all_known_contests())

    def test_getters_common(self):
        self.assertEqual(self.grouper.get_contest_year_by_id('123456'), 2013)
        self.assertEqual(self.grouper.get_contest_season_by_id('123456'), 'Зима')
        self.assertEqual(self.grouper.get_contest_parallel_by_id('789012'), 'olymp')
        self.assertEqual(self.grouper.get_contest_day_by_id('123456'), '3')

    def test_getters_spaces(self):
        self.assertEqual(self.grouper.get_contest_year_by_id('345678'), 2011)
        self.assertEqual(self.grouper.get_contest_season_by_id('345678'), 'Июль')
        self.assertEqual(self.grouper.get_contest_parallel_by_id('123456'), 'A\'')
        self.assertEqual(self.grouper.get_contest_day_by_id('789012'), '3')

    def test_getters_no_values(self):
        self.assertEqual(self.grouper.get_contest_year_by_id('789012'), 0)
        self.assertEqual(self.grouper.get_contest_season_by_id('789012'), '')
        self.assertEqual(self.grouper.get_contest_season_by_id('789012'), '')
        self.assertEqual(self.grouper.get_contest_day_by_id('345678'), '')

    def test_group_common(self):
        grouped_by_year = self.grouper.group_contests_by_year(self.grouper.get_all_known_contests())
        self.assertEqual(len(grouped_by_year), 3)
        self.assertTrue(2013 in grouped_by_year)
        self.assertEqual(grouped_by_year[2013], ['123456'])
        self.assertTrue(0 in grouped_by_year)
        self.assertEqual(grouped_by_year[0], ['789012'])
        self.assertTrue(2011 in grouped_by_year)
        self.assertEqual(grouped_by_year[2011], ['345678'])

        grouped_by_season = self.grouper.group_contests_by_season(self.grouper.get_all_known_contests())
        self.assertEqual(len(grouped_by_season), 3)
        self.assertTrue('Зима' in grouped_by_season)
        self.assertEqual(grouped_by_season['Зима'], ['123456'])
        self.assertTrue('' in grouped_by_season)
        self.assertEqual(grouped_by_season[''], ['789012'])
        self.assertTrue('Июль' in grouped_by_season)
        self.assertEqual(grouped_by_season['Июль'], ['345678'])

        grouped_by_parallel = self.grouper.group_contests_by_parallel(self.grouper.get_all_known_contests())
        self.assertEqual(len(grouped_by_parallel), 3)
        self.assertTrue('A\'' in grouped_by_parallel)
        self.assertEqual(grouped_by_parallel['A\''], ['123456'])
        self.assertTrue('olymp' in grouped_by_parallel)
        self.assertEqual(grouped_by_parallel['olymp'], ['789012'])
        self.assertTrue('' in grouped_by_parallel)
        self.assertEqual(grouped_by_parallel[''], ['345678'])


if __name__ == "__main__":
    unittest.main()
