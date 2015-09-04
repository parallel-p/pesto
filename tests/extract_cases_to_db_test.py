import unittest
from unittest.mock import Mock, patch

from pesto_testcase import PestoTestCase
from extract_cases_to_db import extract_cases_to_db


class ExtractCasesToDBTest(PestoTestCase):
    def prepare_request(self, format_string, data_tuple):
        return format_string.replace('?', '{}').format(*data_tuple)

    @patch('builtins.print')
    def test_common(self, pr):
        cursor = Mock()
        cursor.execute.return_value.fetchone = Mock(side_effect=[(1,), (1,), (2,)])
        cursor.execute.return_value.fetchall.return_value.__len__ = Mock(return_value=1)
        problem = Mock(problem_id=['3', '4'], polygon_id='22', cases=['qwer', 'asdf', 'zxcv'])
        problem.name = 'A'
        # problem_generator = Mock(return_value=problem)
        with unittest.mock.patch('extract_cases_to_db.problem_generator', return_value=[problem]):
            extract_cases_to_db(None, cursor, 'abacaba')
        resulting_requests = []
        for one_call in cursor.execute.call_args_list[1:]:
            format_string, data_tuple = tuple(one_call)[0]
            resulting_requests.append(self.prepare_request(format_string, data_tuple))
        good_requests = ['SELECT id FROM Contests WHERE origin = abacaba AND contest_id = 000003',
                         'SELECT id FROM Problems WHERE contest_ref = 1 AND problem_id = 4',
                         'UPDATE Problems SET name = A, polygon_id = 22 WHERE contest_ref = 1 AND problem_id = 4',
                         'SELECT id FROM Problems WHERE contest_ref = 1 AND problem_id = 4',
                         'UPDATE Cases SET io_hash = qwer WHERE problem_ref = 2 AND case_id = 1',
                         'UPDATE Cases SET io_hash = asdf WHERE problem_ref = 2 AND case_id = 2',
                         'UPDATE Cases SET io_hash = zxcv WHERE problem_ref = 2 AND case_id = 3']
        self.maxDiff = None
        self.assertEqual(resulting_requests, good_requests)

    @patch('builtins.print')
    def test_empty(self, pr):
        cursor = Mock()
        cursor.execute.return_value.fetchone = Mock(side_effect=[(0,)])
        with unittest.mock.patch('extract_cases_to_db.problem_generator', return_value=[None]):
            extract_cases_to_db(None, cursor, 'abacaba')
        cursor.execute.assert_called_once_with('SELECT COUNT(id) FROM Contests')

    @patch('builtins.print')
    def test_no_problem(self, pr):
        cursor = Mock()
        cursor.execute.return_value.fetchone = Mock(side_effect=[(1,), (1,), (2,)])
        cursor.execute.return_value.fetchall.return_value.__len__ = Mock(return_value=0)
        problem = Mock(problem_id=['3', '4'], polygon_id='22', cases=['qwer', 'asdf', 'zxcv'])
        problem.name = 'A'
        with unittest.mock.patch('extract_cases_to_db.problem_generator', return_value=[problem]):
            extract_cases_to_db(None, cursor, 'abacaba')
        resulting_requests = []
        for one_call in cursor.execute.call_args_list[1:]:
            format_string, data_tuple = tuple(one_call)[0]
            resulting_requests.append(self.prepare_request(format_string, data_tuple))
        good_requests = ['SELECT id FROM Contests WHERE origin = abacaba AND contest_id = 000003',
                         'SELECT id FROM Problems WHERE contest_ref = 1 AND problem_id = 4',
                         'INSERT INTO Problems (id, contest_ref, polygon_id, problem_id, name) VALUES (NULL, 1, 22, 4, A)',
                         'SELECT id FROM Problems WHERE contest_ref = 1 AND problem_id = 4',
                         'UPDATE Cases SET io_hash = qwer WHERE problem_ref = 2 AND case_id = 1',
                         'UPDATE Cases SET io_hash = asdf WHERE problem_ref = 2 AND case_id = 2',
                         'UPDATE Cases SET io_hash = zxcv WHERE problem_ref = 2 AND case_id = 3']
        self.maxDiff = None
        self.assertEqual(resulting_requests, good_requests)


if __name__ == "__main__":
    unittest.main()
