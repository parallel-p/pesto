import unittest
from unittest.mock import Mock, call
from dao_problems import DAOProblems
from dao_cases import DAOCases
import dao_problems


class DAOProblemsTest(unittest.TestCase):
    def setUp(self):
        self.row = {'id': 2, 'contest_ref': 1, 'problem_id': 'problem_id', 'name': 'name'}
        self.cursor = Mock()
        connection = Mock()
        connection.get_cursor.return_value = self.cursor
        self.dao = DAOProblems(connection)
        dao_problems.Problem = Mock(return_value=Mock())

    def test_load(self):
        res = self.dao.load(self.row)
        self.assertEqual(dao_problems.Problem.mock_calls, [call(('', 'problem_id'), 'name', [])])
        self.assertEqual(res.contest_ref, 1)

    def test_deep_load(self):
        res = Mock()
        res.cases = []
        self.dao.load = Mock(return_value=res)
        self.cursor.fetchone.side_effect = [{'contest_id': '1'}, 1, 2, None]
        DAOCases.columns = 'kek'
        DAOCases.load = Mock(side_effect=['hash1', 'hash2'])
        self.assertEqual(self.dao.deep_load(self.row), res)
        self.assertEqual(res.problem_id, ('1', 'problem_id'))
        self.assertEqual(res.cases, ['hash1', 'hash2'])
        calls = [call.execute('SELECT contest_id FROM Contests WHERE id = ?', 1),
                 call.fetchone(),
                 call.execute('SELECT kek FROM Cases WHERE problem_ref = ?', 2),
                 call.fetchone(), call.fetchone(), call.fetchone()]
        self.assertEqual(self.cursor.mock_calls, calls)
        self.assertEqual(DAOCases.load.mock_calls, [call(1), call(2)])

    def test_define(self):
        self.dao.lookup = Mock(side_effect=[None, 2])
        self.dao.create = Mock(return_value=1)
        self.assertEqual(self.dao.define('contest_ref1', 'problem_id1'), 1)
        self.assertEqual(self.dao.define('contest_ref2', 'problem_id2'), 2)
        calls = [call('contest_ref1', 'problem_id1'), call('contest_ref2', 'problem_id2')]
        self.assertEqual(self.dao.lookup.mock_calls, calls)
        calls = [call('contest_ref1', 'problem_id1')]
        self.assertEqual(self.dao.create.mock_calls, calls)

    def test_lookup(self):
        self.cursor.fetchone.side_effect = [{'id': 1}, None]
        self.assertEqual(self.dao.lookup('contest_ref1', 'problem_id1'), 1)
        self.assertEqual(self.dao.lookup('contest_ref2', 'problem_id2'), None)
        calls = [call.execute('SELECT id FROM Problems WHERE contest_ref = ? AND problem_id = ?',
                              ['contest_ref1', 'problem_id1']),
                 call.fetchone(),
                 call.execute('SELECT id FROM Problems WHERE contest_ref = ? AND problem_id = ?',
                              ['contest_ref2', 'problem_id2']),
                 call.fetchone()]
        self.assertEqual(self.cursor.mock_calls, calls)

    def test_create(self):
        self.cursor.lastrowid = 1
        self.assertEqual(self.dao.create('contest_ref', 'problem_id'), 1)
        calls = [call.execute('INSERT INTO Problems (id, contest_ref, problem_id) VALUES (NULL, ?, ?)',
                              ['contest_ref', 'problem_id'])]
        self.assertEqual(self.cursor.mock_calls, calls)

    def test_update(self):
        self.cursor.fetchone.return_value = None
        contest1, contest2 = Mock(), Mock()
        contest1.contest_ref, contest1.name, contest1.problem_id = 'contest_ref1', 'name1', ('', 'problem_id1')
        contest2.contest_ref, contest2.name, contest2.problem_id = 'contest_ref2', 'name2', ('', 'problem_id2')
        self.dao.load = Mock(side_effect=[contest1, contest2])
        self.dao.update(1, {'contest_ref': 'contest_ref3'})
        self.dao.update(2, {'name': 'name3', 'problem_id': 'problem_id3'})
        calls = [call.execute('SELECT id, contest_ref, problem_id, name FROM Problems WHERE id = ?', 1),
                 call.fetchone(),
                 call.execute('UPDATE Problems SET contest_ref = :contest_ref, name = :name, problem_id = :problem_id '
                              'WHERE id = :id', {'contest_ref': 'contest_ref3',
                                                 'name': 'name1', 'problem_id': 'problem_id1', 'id': 1}),
                 call.execute('SELECT id, contest_ref, problem_id, name FROM Problems WHERE id = ?', 2),
                 call.fetchone(),
                 call.execute('UPDATE Problems SET contest_ref = :contest_ref, name = :name, problem_id = :problem_id '
                              'WHERE id = :id', {'contest_ref': 'contest_ref2',
                                                 'name': 'name3', 'problem_id': 'problem_id3', 'id': 2})]
        self.assertEqual(self.cursor.mock_calls, calls)

if __name__ == "__main__":
    unittest.main()
