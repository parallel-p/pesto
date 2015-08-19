import unittest
from unittest.mock import Mock, call, patch
from pesto_testcase import PestoTestCase
from dao_submits import DAOSubmits
import dao_submits


class DAOSubmitsTest(unittest.TestCase):
    def setUp(self):
        self.row = {'id': 1, 'submit_id': 'submit_id', 'lang_id': 'lang_id', 'problem_ref': 'problem_ref',
                    'user_ref': 'user_ref', 'outcome': 'outcome', 'timestamp': 'timestamp'}
        self.cursor = Mock()
        connection = Mock()
        connection.get_cursor.return_value = self.cursor
        self.dao = DAOSubmits(connection)

    @patch('dao_submits.Submit', Mock())
    def test_load(self):
        res = self.dao.load(self.row)
        self.assertEqual(dao_submits.Submit.mock_calls,
                         [call('submit_id', ('', ''), '', 'lang_id', [], 'outcome', '', 'timestamp')])
        self.assertEqual(res.problem_ref, 'problem_ref')
        self.assertEqual(res.user_ref, 'user_ref')

    @patch('dao_submits.DAORuns', columns='kek')
    def test_deep_load(self, dr):
        res = Mock()
        res.runs = list()
        self.dao.load = Mock(return_value=res)
        dao_runs = Mock()
        dao_runs.load_all.return_value = [1, 2]
        dao_submits.DAORuns.return_value = dao_runs
        self.cursor.fetchall.return_value = ['row1', 'row2']
        res = self.dao.deep_load(self.row)
        self.assertEqual(self.cursor.mock_calls,
                         [call.execute('SELECT kek FROM Runs WHERE submit_ref = ?', [1]), call.fetchall()])
        self.assertEqual(dao_runs.mock_calls, [call.load_all(['row1', 'row2'], 'problem_ref')])
        self.assertEqual(res.runs, [1, 2])
        self.assertEqual(res.mock_calls, [call.count_results()])

    def test_define(self):
        self.dao.lookup = Mock(side_effect=[None, 2])
        self.dao.create = Mock(return_value=1)
        self.assertEqual(self.dao.define('submit_id1', 'problem_ref1'), 1)
        self.assertEqual(self.dao.define('submit_id2', 'problem_ref2'), 2)
        calls = [call('submit_id1', 'problem_ref1'), call('submit_id2', 'problem_ref2')]
        self.assertEqual(self.dao.lookup.mock_calls, calls)
        calls = [call('submit_id1', 'problem_ref1')]
        self.assertEqual(self.dao.create.mock_calls, calls)

    def test_lookup(self):
        self.cursor.fetchone.side_effect = [{'id': 1}, None]
        self.assertEqual(self.dao.lookup('submit_id1', 'problem_ref1'), 1)
        self.assertEqual(self.dao.lookup('submit_id2', 'problem_ref2'), None)
        calls = [call.execute('SELECT id FROM Submits WHERE submit_id = ? AND problem_ref = ?',
                              ['submit_id1', 'problem_ref1']),
                 call.fetchone(),
                 call.execute('SELECT id FROM Submits WHERE submit_id = ? AND problem_ref = ?',
                              ['submit_id2', 'problem_ref2']),
                 call.fetchone()]
        self.assertEqual(self.cursor.mock_calls, calls)

    def test_create(self):
        self.cursor.lastrowid = 1
        self.assertEqual(self.dao.create('submit_id', 'problem_ref'), 1)
        calls = [call.execute('INSERT INTO Submits (id, submit_id, problem_ref) VALUES (NULL, ?, ?)',
                              ['submit_id', 'problem_ref'])]
        self.assertEqual(self.cursor.mock_calls, calls)

    def test_update(self):
        self.cursor.fetchone.return_value = None
        submit1, submit2 = Mock(), Mock()
        submit1.submit_id, submit1.lang_id, submit1.problem_ref = 'submit_id1', 'lang_id1', 'problem_ref1'
        submit1.user_ref, submit1.outcome, submit1.timestamp = 'user_ref1', 'outcome1', 'timestamp1'
        submit2.submit_id, submit2.lang_id, submit2.problem_ref = 'submit_id2', 'lang_id2', 'problem_ref2'
        submit2.user_ref, submit2.outcome, submit2.timestamp = 'user_ref2', 'outcome2', 'timestamp2'
        self.dao.load = Mock(side_effect=[submit1, submit2])
        self.dao.update(1, {'submit_id': 'submit_id3', 'lang_id': 'lang_id3', 'problem_ref': 'problem_ref3'})
        self.dao.update(2, {'user_ref': 'user_ref3', 'outcome': 'outcome3', 'timestamp': 'timestamp3'})
        calls = [call.execute('SELECT id, submit_id, lang_id, problem_ref, user_ref, outcome, '
                              'timestamp FROM Submits WHERE id = ?', [1]), call.fetchone(),
                 call.execute('UPDATE Submits SET submit_id = :submit_id, lang_id = :lang_id,'
                              ' problem_ref = :problem_ref, user_ref = :user_ref, outcome = :outcome,'
                              ' timestamp = :timestamp WHERE id = :id',
                              {'submit_id': 'submit_id3', 'lang_id': 'lang_id3', 'problem_ref': 'problem_ref3',
                               'user_ref': 'user_ref1', 'outcome': 'outcome1', 'timestamp': 'timestamp1', 'id': 1}),
                 call.execute('SELECT id, submit_id, lang_id, problem_ref, user_ref, outcome, '
                              'timestamp FROM Submits WHERE id = ?', [2]), call.fetchone(),
                 call.execute('UPDATE Submits SET submit_id = :submit_id, lang_id = :lang_id,'
                              ' problem_ref = :problem_ref, user_ref = :user_ref, outcome = :outcome,'
                              ' timestamp = :timestamp WHERE id = :id',
                              {'submit_id': 'submit_id2', 'lang_id': 'lang_id2', 'problem_ref': 'problem_ref2',
                               'user_ref': 'user_ref3', 'outcome': 'outcome3', 'timestamp': 'timestamp3', 'id': 2})]
        self.assertEqual(self.cursor.mock_calls, calls)

if __name__ == "__main__":
    unittest.main()
