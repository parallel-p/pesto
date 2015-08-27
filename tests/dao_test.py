import unittest
from unittest.mock import Mock, call, patch

from dao import UsersDAO, ContestsDAO, ProblemsDAO
import dao
import model


class DAOUsersTest(unittest.TestCase):
    def setUp(self):
        self.row = {'origin': 'origin', 'user_id': 'user_id'}
        self.cursor = Mock()
        connection = Mock()
        connection.get_cursor.return_value = self.cursor
        self.dao = UsersDAO(connection)

    @patch('dao.User', Mock(return_value='User_object'))
    def test_load(self):
        self.assertEqual(self.dao.load(self.row), 'User_object')
        self.assertEqual(dao.User.mock_calls, [call('user_id', 'origin')])

    def test_deep_load(self):
        self.dao.load = Mock(return_value='Load')
        self.assertEqual(self.dao.deep_load('row'), 'Load')
        self.assertEqual(self.dao.load.mock_calls, [call('row')])

    def test_define(self):
        self.dao.lookup = Mock(side_effect=[None, 2])
        self.dao.create = Mock(return_value=1)
        self.assertEqual(self.dao.define('origin1', 'user_id1'), 1)
        self.assertEqual(self.dao.define('origin2', 'user_id2'), 2)
        calls = [call('origin1', 'user_id1'), call('origin2', 'user_id2')]
        self.assertEqual(self.dao.lookup.mock_calls, calls)
        calls = [call('origin1', 'user_id1')]
        self.assertEqual(self.dao.create.mock_calls, calls)

    def test_lookup(self):
        self.cursor.fetchone.side_effect = [{'id': 1}, None]
        self.assertEqual(self.dao.lookup('origin1', 'user_id1'), 1)
        self.assertEqual(self.dao.lookup('origin2', 'user_id2'), None)
        calls = [call.execute('SELECT id FROM Users WHERE origin = ? AND user_id = ?',
                              ['origin1', 'user_id1']),
                 call.fetchone(),
                 call.execute('SELECT id FROM Users WHERE origin = ? AND user_id = ?',
                              ['origin2', 'user_id2']),
                 call.fetchone()]
        self.assertEqual(self.cursor.mock_calls, calls)

    def test_create(self):
        self.cursor.lastrowid = 1
        self.assertEqual(self.dao.create('origin', 'user_id'), 1)
        calls = [call.execute('INSERT INTO Users (id, origin, user_id) VALUES (NULL, ?, ?)',
                              ['origin', 'user_id'])]
        self.assertEqual(self.cursor.mock_calls, calls)

    def test_update(self):
        self.cursor.fetchone.return_value = None
        user1, user2 = Mock(), Mock()
        user1.origin, user1.user_id = 'origin1', 'user_id1'
        user2.origin, user2.user_id = 'origin2', 'user_id2'
        self.dao.load = Mock(side_effect=[user1, user2])
        self.dao.update(1, {'origin': 'origin3'})
        self.dao.update(2, {'user_id': 'user_id3'})
        calls = [call.execute('SELECT origin, user_id FROM Users WHERE id = ?', [1]),
                 call.fetchone(),
                 call.execute('UPDATE Users SET origin = :origin, user_id = :user_id '
                              'WHERE id = :id', {'origin': 'origin3', 'user_id': 'user_id1', 'id': 1}),
                 call.execute('SELECT origin, user_id FROM Users WHERE id = ?', [2]),
                 call.fetchone(),
                 call.execute('UPDATE Users SET origin = :origin, user_id = :user_id '
                              'WHERE id = :id', {'origin': 'origin2', 'user_id': 'user_id3', 'id': 2})]
        self.assertEqual(self.cursor.mock_calls, calls)


class ContestsDAOTest(unittest.TestCase):
    def setUp(self):
        self.row = {'contest_id': '42', 'origin': 'orig', 'name': 'Untitled', 'scoring': 'ACM'}
        self.cursor = Mock()
        connection = Mock()
        connection.get_cursor.return_value = self.cursor
        self.dao = ContestsDAO(connection)

    @patch('model.Contest', Mock(return_value='Contest_object'))
    def test_load(self):
        return_value = self.dao.load(self.row)
        self.assertEqual(return_value, 'Contest_object')
        model.Contest.assert_called_once_with('42', 'orig', 'Untitled', 'ACM')

    @patch('model.Contest', Mock(return_value='Contest_object'))
    def test_deep_load(self):
        return_value = self.dao.deep_load(self.row)
        self.assertEqual(return_value, 'Contest_object')
        model.Contest.assert_called_once_with('42', 'orig', 'Untitled', 'ACM')

    def test_define(self):
        self.dao.lookup = Mock(side_effect=[None, 2])
        self.dao.create = Mock(return_value=1)
        self.assertEqual(self.dao.define('origin1', 'scoring1', 'contest_id1'), 1)
        self.assertEqual(self.dao.define('origin2', 'scoring2', 'contest_id2'), 2)
        calls = [call('origin1', 'scoring1', 'contest_id1'), call('origin2', 'scoring2', 'contest_id2')]
        self.assertEqual(self.dao.lookup.mock_calls, calls)
        calls = [call('origin1', 'scoring1', 'contest_id1')]
        self.assertEqual(self.dao.create.mock_calls, calls)

    def test_lookup(self):
        self.cursor.fetchone.side_effect = [{'id': 1}, None]
        self.assertEqual(self.dao.lookup('origin1', 'scoring1', 'contest_id1'), 1)
        self.assertEqual(self.dao.lookup('origin2', 'scoring2', 'contest_id2'), None)
        calls = [call.execute('SELECT id FROM Contests WHERE origin = ? AND scoring = ? AND contest_id = ?',
                              ['origin1', 'scoring1', 'contest_id1']),
                 call.fetchone(),
                 call.execute('SELECT id FROM Contests WHERE origin = ? AND scoring = ? AND contest_id = ?',
                              ['origin2', 'scoring2', 'contest_id2']),
                 call.fetchone()]
        self.assertEqual(self.cursor.mock_calls, calls)

    def test_create(self):
        self.cursor.lastrowid = 1
        self.assertEqual(self.dao.create('origin', 'scoring', 'contest_id'), 1)
        calls = [call.execute('INSERT INTO Contests (id, origin, scoring, contest_id) VALUES (NULL, ?, ?, ?)',
                              ['origin', 'scoring', 'contest_id'])]
        self.assertEqual(self.cursor.mock_calls, calls)

    def test_update(self):
        self.cursor.fetchone.return_value = None
        contest1, contest2 = Mock(), Mock()
        contest1.origin, contest1.name = 'origin1', 'name1'
        contest1.scoring, contest1.contest_id = 'scoring1', 'contest_id1'
        contest2.origin, contest2.name = 'origin2', 'name2'
        contest2.scoring, contest2.contest_id = 'scoring2', 'contest_id2'
        self.dao.load = Mock(side_effect=[contest1, contest2])
        self.dao.update(1, {'name': 'name3'})
        self.dao.update(2, {'scoring': 'scoring3', 'contest_id': 'contest_id3'})
        calls = [call.execute('SELECT contest_id, origin, name, scoring FROM Contests WHERE id = ?', [1]),
                 call.fetchone(),
                 call.execute('UPDATE Contests SET origin = :origin, name = :name, scoring = :scoring, '
                              'contest_id = :contest_id WHERE id = :id', {'origin': 'origin1', 'name': 'name3',
                                                                          'scoring': 'scoring1',
                                                                          'contest_id': 'contest_id1', 'id': 1}),
                 call.execute('SELECT contest_id, origin, name, scoring FROM Contests WHERE id = ?', [2]),
                 call.fetchone(),
                 call.execute('UPDATE Contests SET origin = :origin, name = :name, scoring = :scoring, '
                              'contest_id = :contest_id WHERE id = :id', {'origin': 'origin2', 'name': 'name2',
                                                                          'scoring': 'scoring3',
                                                                          'contest_id': 'contest_id3', 'id': 2})]
        self.assertEqual(self.cursor.mock_calls, calls)


class ProblemsDAOTest(unittest.TestCase):
    def setUp(self):
        self.row = {'id': 2, 'contest_ref': 1, 'problem_id': 'problem_id', 'name': 'name'}
        self.cursor = Mock()
        connection = Mock()
        connection.get_cursor.return_value = self.cursor
        self.dao = ProblemsDAO(connection)

    @patch('dao.Problem', Mock())
    def test_load(self):
        res = self.dao.load(self.row)
        self.assertEqual(dao.Problem.mock_calls, [call(('', 'problem_id'), '', 'name', [])])
        self.assertEqual(res.contest_ref, 1)

    @patch('dao.DAOCases', columns='kek')
    def test_deep_load(self, dc):
        res = Mock()
        res.cases = []
        self.dao.load = Mock(return_value=res)
        self.cursor.fetchone.side_effect = [{'contest_id': '1'}, 1, 2, None]
        dc.load = Mock(side_effect=['hash1', 'hash2'])
        self.assertEqual(self.dao.deep_load(self.row), res)
        self.assertEqual(res.problem_id, ('1', 'problem_id'))
        self.assertEqual(res.cases, ['hash1', 'hash2'])
        calls = [call.execute('SELECT contest_id FROM Contests WHERE id = ?', [1]),
                 call.fetchone(),
                 call.execute('SELECT kek FROM Cases WHERE problem_ref = ?', [2]),
                 call.fetchone(), call.fetchone(), call.fetchone()]
        self.assertEqual(self.cursor.mock_calls, calls)
        self.assertEqual(dao.DAOCases.load.mock_calls, [call(1), call(2)])

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
        problem1, problem2 = Mock(), Mock()
        problem1.contest_ref, problem1.name, problem1.problem_id = 'contest_ref1', 'name1', ('', 'problem_id1')
        problem2.contest_ref, problem2.name, problem2.problem_id = 'contest_ref2', 'name2', ('', 'problem_id2')
        self.dao.load = Mock(side_effect=[problem1, problem2])
        self.dao.update(1, {'contest_ref': 'contest_ref3'})
        self.dao.update(2, {'name': 'name3', 'problem_id': 'problem_id3'})
        calls = [call.execute('SELECT id, contest_ref, problem_id, name FROM Problems WHERE id = ?', [1]),
                 call.fetchone(),
                 call.execute('UPDATE Problems SET contest_ref = :contest_ref, name = :name, problem_id = :problem_id '
                              'WHERE id = :id', {'contest_ref': 'contest_ref3',
                                                 'name': 'name1', 'problem_id': 'problem_id1', 'id': 1}),
                 call.execute('SELECT id, contest_ref, problem_id, name FROM Problems WHERE id = ?', [2]),
                 call.fetchone(),
                 call.execute('UPDATE Problems SET contest_ref = :contest_ref, name = :name, problem_id = :problem_id '
                              'WHERE id = :id', {'contest_ref': 'contest_ref2',
                                                 'name': 'name3', 'problem_id': 'problem_id3', 'id': 2})]
        self.assertEqual(self.cursor.mock_calls, calls)


if __name__ == "__main__":
    unittest.main()
