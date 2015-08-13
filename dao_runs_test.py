import unittest
from unittest.mock import Mock, call
from pesto_testcase import PestoTestCase
from dao_runs import DAORuns
import dao_runs


class RunsDaoTest(PestoTestCase):
    def setUp(self):
        self.row = {'realtime': 'realtime', 'time': 'time', 'outcome': 'outcome',
                    'submit_ref': 'submit_ref', 'case_ref': 'case_ref'}
        self.cursor = Mock()
        connection = Mock()
        connection.get_cursor.return_value = self.cursor
        self.dao = DAORuns(connection)
        dao_runs.Run = Mock(return_value=Mock())

    def test_load(self):
        res = self.dao.load(self.row)
        self.assertEqual(dao_runs.Run.mock_calls, [call('', '', '', 'realtime', 'time', 'outcome')])
        self.assertEqual(res.submit_ref, 'submit_ref')
        self.assertEqual(res.case_ref, 'case_ref')

    def test_deep_load(self):
        self.dao.load = Mock(return_value=Mock())
        self.cursor.fetchone.return_value = {'case_id': 'case_id'}
        res = self.dao.deep_load(self.row)
        self.assertEqual(res.case_id, 'case_id')
        self.assertEqual(self.cursor.mock_calls,
                         [call.execute('SELECT case_id FROM Cases WHERE id = ?', ['case_ref']), call.fetchone()])

    def test_define(self):
        self.dao.lookup = Mock(side_effect=[None, 2])
        self.dao.create = Mock(return_value=1)
        self.assertEqual(self.dao.define('submit_ref1', 'case_ref1'), 1)
        self.assertEqual(self.dao.define('submit_ref2', 'case_ref2'), 2)
        calls = [call('submit_ref1', 'case_ref1'), call('submit_ref2', 'case_ref2')]
        self.assertEqual(self.dao.lookup.mock_calls, calls)
        calls = [call('submit_ref1', 'case_ref1')]
        self.assertEqual(self.dao.create.mock_calls, calls)

    def test_lookup(self):
        self.cursor.fetchone.side_effect = [{'id': 1}, None]
        self.assertEqual(self.dao.lookup('submit_ref1', 'case_ref1'), 1)
        self.assertEqual(self.dao.lookup('submit_ref2', 'case_ref2'), None)
        calls = [call.execute('SELECT id FROM Runs WHERE submit_ref = ? AND case_ref = ?',
                              ['submit_ref1', 'case_ref1']),
                 call.fetchone(),
                 call.execute('SELECT id FROM Runs WHERE submit_ref = ? AND case_ref = ?',
                              ['submit_ref2', 'case_ref2']),
                 call.fetchone()]
        self.assertEqual(self.cursor.mock_calls, calls)

    def test_create(self):
        self.cursor.lastrowid = 1
        self.assertEqual(self.dao.create('submit_ref', 'case_ref'), 1)
        calls = [call.execute('INSERT INTO Runs (id, submit_ref, case_ref) VALUES (NULL, ?, ?)',
                              ['submit_ref', 'case_ref'])]
        self.assertEqual(self.cursor.mock_calls, calls)

    def test_update(self):
        self.cursor.fetchone.return_value = None
        run1, run2 = Mock(), Mock()
        run1.real_time, run1.time, run1.outcome = 'realtime1', 'time1', 'outcome1'
        run1.submit_ref, run1.case_ref = 'submit_ref1', 'case_ref1'
        run2.real_time, run2.time, run2.outcome = 'realtime2', 'time2', 'outcome2'
        run2.submit_ref, run2.case_ref = 'submit_ref2', 'case_ref2'
        self.dao.load = Mock(side_effect=[run1, run2])
        self.dao.update(1, {'realtime': 'realtime3', 'time': 'time3', 'outcome': 'outcome3'})
        self.dao.update(2, {'submit_ref': 'submit_ref3', 'case_ref': 'case_ref3'})
        calls = [call.execute('SELECT realtime, time, outcome, submit_ref, case_ref FROM Runs WHERE id = ?', [1]),
                 call.fetchone(),
                 call.execute('UPDATE Runs SET submit_ref = :submit_ref, case_ref = :case_ref, realtime = :realtime, '
                              'time = :time, outcome = :outcome WHERE id = :id',
                              {'realtime': 'realtime3', 'time': 'time3', 'outcome': 'outcome3',
                               'submit_ref': 'submit_ref1', 'case_ref': 'case_ref1', 'id': 1}),
                 call.execute('SELECT realtime, time, outcome, submit_ref, case_ref FROM Runs WHERE id = ?', [2]),
                 call.fetchone(),
                 call.execute('UPDATE Runs SET submit_ref = :submit_ref, case_ref = :case_ref, realtime = :realtime, '
                              'time = :time, outcome = :outcome WHERE id = :id',
                              {'realtime': 'realtime2', 'time': 'time2', 'outcome': 'outcome2',
                               'submit_ref': 'submit_ref3', 'case_ref': 'case_ref3', 'id': 2})]
        self.assertEqual(self.cursor.mock_calls, calls)

if __name__ == "__main__":
    unittest.main()
