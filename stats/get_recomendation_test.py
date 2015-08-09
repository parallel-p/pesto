import unittest
from unittest.mock import Mock
from stats.get_recomendation import get_recomendation
from pesto_testcase import PestoTestCase


class GetRecomendationTest(PestoTestCase):
    def prepare_request(self, format_string, data_tuple):
        return format_string.replace('?', '{}').format(*data_tuple)

    @unittest.mock.patch('stats.get_recomendation.last_problem', return_value=['1', '2'])
    def test_common(self, useless_arg):
        pesto_db_cursor = Mock()
        pesto_db_cursor.execute.return_value.fetchall.return_value = ['Test', 'passed.']
        result = get_recomendation('0', Mock(), pesto_db_cursor)
        self.assertEqual(result, ['Test', 'passed.'])
        good_request = 'SELECT recomended_contest_id, recomended_problem_id FROM more_popular_next_problems_recomendations WHERE contest_id = "1" AND problem_id = "2"'
        self.assertEqual(self.prepare_request(*(pesto_db_cursor.execute.call_args[0])), good_request)
