import unittest
from unittest.mock import Mock
from pesto_testcase import PestoTestCase
from extract_cases_to_db import extract_cases_to_db


class ExtractCasesToDBTest(PestoTestCase):
    def prepare_request(self, format_string, data_tuple):
        return format_string.replace('?', '{}').format(*data_tuple)

    def test_common(self):
        cursor = Mock()
        cursor.execute = Mock(side_effect=[(1,), None, (2,), None, None, None, None])
        problem = Mock(problem_id=[3, 4], cases=['qwer', 'asdf', 'zxcv'])
        problem.name = 'A'
        # problem_generator = Mock(return_value=problem)
        with unittest.mock.patch('extract_cases_to_db.problem_generator', return_value=[problem]):
            extract_cases_to_db(None, cursor, 'abacaba')
        resulting_requests = []
        for one_call in cursor.execute.call_args_list:
            format_string, data_tuple = tuple(one_call)[0]
            resulting_requests.append(self.prepare_request(format_string, data_tuple))
        good_requests = ['SELECT id FROM Contests WHERE origin = abacaba AND contest_id = 3',\
                        'UPDATE Problems SET name = A WHERE contest_ref = 1 AND problem_id = 4',\
                        'SELECT id FROM Problems WHERE contest_ref = 1 AND problem_id = 4',\
                        'UPDATE Cases SET io_hash = qwer WHERE problem_ref = 2 AND case_id = 1',\
                        'UPDATE Cases SET io_hash = asdf WHERE problem_ref = 2 AND case_id = 2',\
                        'UPDATE Cases SET io_hash = zxcv WHERE problem_ref = 2 AND case_id = 3']
        self.assertEqual(resulting_requests, good_requests)
