import unittest
from unittest.mock import Mock
from pesto_testcase import PestoTestCase
from stats.problems_grouper import ProblemsGrouper
import os


class ProblemsGrouperTest(PestoTestCase):
    @unittest.mock.patch('stats.problems_grouper.ejudge_get_contest_name',
                        side_effect=['ЛКШ.2013.Зима.  P', 'ЛКШ .Олимпиада', 'ЛКШ.2011 . Июль', 'Левый контест', None, 'ЛКШ.Template'])
    @unittest.mock.patch('stats.problems_grouper.AllFilesWalker',
                        return_value=Mock(walk=Mock(return_value=[(None, os.path.join('a', '123456.xml')),
                                                    (None, os.path.join('a', '789012.xml')),
                                                    (None, os.path.join('a', '345678.xml')),
                                                    (None, None),
                                                    (None, None),
                                                    (None, None)])))
    def setUp(self, useless, args):
        self.grouper = ProblemsGrouper('dir_name')

    def test_get_all(self): 
        self.assertEqual(len(self.grouper.get_all_known_contests()), 3)
        self.assertTrue('123456' in self.grouper.get_all_known_contests())
        self.assertTrue('789012' in self.grouper.get_all_known_contests())
        self.assertTrue('345678' in self.grouper.get_all_known_contests())

    def test_getters_common(self):
        self.assertEqual(self.grouper.get_contest_year_by_id('123456'), 2013)
        self.assertEqual(self.grouper.get_contest_season_by_id('123456'), 'Зима')
        self.assertEqual(self.grouper.get_contest_parallel_by_id('789012'), 'olymp')

    def test_getters_spaces(self):
        self.assertEqual(self.grouper.get_contest_year_by_id('345678'), 2011)
        self.assertEqual(self.grouper.get_contest_season_by_id('345678'), 'Июль')
        self.assertEqual(self.grouper.get_contest_parallel_by_id('123456'), 'P')

    def test_getters_no_values(self):
        self.assertEqual(self.grouper.get_contest_year_by_id('789012'), 0)
        self.assertEqual(self.grouper.get_contest_season_by_id('789012'), '')
        self.assertEqual(self.grouper.get_contest_season_by_id('789012'), '')

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
        self.assertTrue('P' in grouped_by_parallel)
        self.assertEqual(grouped_by_parallel['P'], ['123456'])
        self.assertTrue('olymp' in grouped_by_parallel)
        self.assertEqual(grouped_by_parallel['olymp'], ['789012'])
        self.assertTrue('' in grouped_by_parallel)
        self.assertEqual(grouped_by_parallel[''], ['345678'])

if __name__ == "__main__":
    unittest.main()
