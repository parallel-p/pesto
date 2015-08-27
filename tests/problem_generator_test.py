import unittest
from unittest.mock import Mock, patch

from problem_generator import problem_generator
import md5_hasher


class TestProblemGenerator(unittest.TestCase):
    @patch('md5_hasher.get_hash', Mock(return_value='hash'))
    @patch('ejudge_contest.EjudgeContest')
    def test_common(self, ec):
        ejudge_contest_object = Mock()
        ejudge_contest_object.get_contest_id = Mock(return_value='42')
        ejudge_contest_object.get_problem_ids = Mock(return_value=[('42', '1'), ('42', '2')])
        ejudge_contest_object.get_short_name_by_problem_id = Mock(return_value='a-plus-b')
        ejudge_contest_object.get_test_paths_by_problem_id = Mock(return_value=[('a', 'b'), ('c', 'd')])
        ec.return_value = ejudge_contest_object
        contest_dirs = [('000001', '000001'), ('000179', '000179')]
        result = [x for x in problem_generator(contest_dirs)]
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0].problem_id, ('42', '1'))
        self.assertEqual(result[1].problem_id, ('42', '2'))
        self.assertEqual(result[2].problem_id, ('42', '1'))
        self.assertEqual(result[3].problem_id, ('42', '2'))
        for problem in result:
            self.assertEqual(problem.name, 'a-plus-b')
            self.assertEqual(problem.cases, ['hash', 'hash'])
        self.assertEqual(md5_hasher.get_hash.call_args_list, [(('a', 'b'),), (('c', 'd'),)] * 4)


"""class TestSqliteProblemGenerator(unittest.TestCase):
    def setUp(self):
        ejudge_contest_object = Mock()
        ejudge_contest_object.get_contest_id = Mock(return_value='42')
        ejudge_contest_object.get_problem_ids = Mock(return_value=[('42', '1'), ('42', '2')])
        ejudge_contest_object.get_short_name_by_problem_id = Mock(return_value='a-plus-b')
        ejudge_contest_object.get_test_paths_by_problem_id = Mock(return_value=[('a', 'b'), ('c', 'd')])
        ejudge_contest.EjudgeContest = Mock(return_value=ejudge_contest_object)
        md5_hasher.get_hash = Mock(return_value='hash')

    @patch('problem_generator.connect')
    @patch('sqlite_connector.SQLiteConnector')
    @patch('problem_generator.ProblemsDAO')
    def test_common(self, dao, connector, conn):
        conn.return_value.fetchall.return_value = [{'id': 1, 'problem_id': '42', 'name': 'a_plus_b'}]
        dao.columns = '123'
        result = list(sqlite_problem_generator('sqlite'))
        self.assertEqual(len(result), 1)
        conn.return_value.execute.assert_called_once_with('SELECT 123 FROM Problems')

    def test_connect(self):
        conn = Mock()
        conn.get_cursor.return_value = 42
        self.assertEqual(connect(conn, '123'), 42)
        conn.create_connection.assert_called_once_with('123')"""

if __name__ == "__main__":
    unittest.main()
