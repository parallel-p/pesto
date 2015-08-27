import unittest
from unittest.mock import Mock, call, patch

from dao import UsersDAO
import dao


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

if __name__ == "__main__":
    unittest.main()
