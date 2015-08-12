import unittest
from unittest.mock import Mock, call
from dao_cases import DAOCases


class DAOCasesTest(unittest.TestCase):
    def setUp(self):
        self.cursor = Mock()
        connection = Mock()
        connection.get_cursor.return_value = self.cursor
        self.dao_cases = DAOCases(connection)

    def test_load(self):
        row = {"id": "1", "case_id": "1", "problem_ref": "1", "io_hash": "440fae04f9e3619de0b8e9319a6a5f4b"}
        self.assertEqual(self.dao_cases.deep_load(row), "440fae04f9e3619de0b8e9319a6a5f4b")
        self.assertEqual(DAOCases.load(row), "440fae04f9e3619de0b8e9319a6a5f4b")

    def test_define(self):
        self.dao_cases.lookup = Mock(side_effect=[None, 2])
        self.dao_cases.create = Mock(return_value=1)
        self.assertEqual(self.dao_cases.define('problem_ref1', 'case_id1'), 1)
        self.assertEqual(self.dao_cases.define('problem_ref2', 'case_id2'), 2)
        calls = [call('problem_ref1', 'case_id1'), call('problem_ref2', 'case_id2')]
        self.assertEqual(self.dao_cases.lookup.mock_calls, calls)
        calls = [call('problem_ref1', 'case_id1')]
        self.assertEqual(self.dao_cases.create.mock_calls, calls)

    def test_lookup(self):
        self.cursor.fetchone.side_effect = [{'id': 1}, None]
        self.assertEqual(self.dao_cases.lookup('problem_ref1', 'case_id1'), 1)
        self.assertEqual(self.dao_cases.lookup('problem_ref2', 'case_id2'), None)
        calls = [call.execute('SELECT id FROM Cases WHERE problem_ref = ? AND case_id = ?',
                              ['problem_ref1', 'case_id1']),
                 call.fetchone(),
                 call.execute('SELECT id FROM Cases WHERE problem_ref = ? AND case_id = ?',
                              ['problem_ref2', 'case_id2']),
                 call.fetchone()]
        self.assertEqual(self.cursor.mock_calls, calls)

    def test_create(self):
        self.cursor.lastrowid = 1
        self.assertEqual(self.dao_cases.create('problem_ref', 'case_id'), 1)
        calls = [call.execute('INSERT INTO Cases (id, problem_ref, case_id) VALUES (NULL, ?, ?)',
                              ['problem_ref', 'case_id'])]
        self.assertEqual(self.cursor.mock_calls, calls)

    def test_update(self):
        self.cursor.fetchone.return_value = None
        DAOCases.load = Mock(side_effect=['io_hash1', 'io_hash2'])
        self.dao_cases.update(1, {'io_hash': 'io_hash3'})
        self.dao_cases.update(2, {})
        calls = [call.execute('SELECT io_hash FROM Cases WHERE id = ?', 1),
                 call.fetchone(),
                 call.execute('UPDATE Cases SET io_hash = :io_hash WHERE id = :id', {'io_hash': 'io_hash3', 'id': 1}),
                 call.execute('SELECT io_hash FROM Cases WHERE id = ?', 2),
                 call.fetchone(),
                 call.execute('UPDATE Cases SET io_hash = :io_hash WHERE id = :id', {'io_hash': 'io_hash2', 'id': 2})]
        self.assertEqual(self.cursor.mock_calls, calls)

if __name__ == "__main__":
    unittest.main()
