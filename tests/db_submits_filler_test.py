import unittest

from unittest.mock import Mock, call

from db_submits_filler import DBSubmitsFiller


class TestDBSubmitsFiller(unittest.TestCase):
    def setUp(self):
        self.filler = DBSubmitsFiller(Mock())

    def test_right_values(self):
        self.filler.db_define_ref = Mock(side_effect=[1, 2, 3, 4, 5, 6, 7, 8])
        self.filler.db_update = Mock()
        submit = Mock()
        submit.scoring = 'scoring'
        submit.problem_id = ['problem_id0', 'problem_id1']
        submit.user_id = 'user_id'
        submit.submit_id = 'submit_id'
        submit.lang_id = 'lang_id'
        submit.outcome = 'outcome'
        submit.timestamp = 'timestamp'
        submit.runs = [Mock(), Mock()]
        submit.runs[0].case_id = 'case_id0'
        submit.runs[1].case_id = 'case_id1'
        submit.runs[0].real_time = 'real_time0'
        submit.runs[1].real_time = 'real_time1'
        submit.runs[0].time = 'time0'
        submit.runs[1].time = 'time1'
        submit.runs[0].outcome = 'outcome0'
        submit.runs[1].outcome = 'outcome1'
        self.filler.fill_db_from_submit(submit, 'origin')
        self.assertEqual(len(self.filler.db_define_ref.mock_calls), 8)
        keys, values = ['origin', 'scoring', 'contest_id'], ['origin', 'scoring', 'problem_id0']
        self.assertEqual(self.filler.db_define_ref.mock_calls[0], call('Contests', keys, values))
        keys, values = ['origin', 'user_id'], ['origin', 'user_id']
        self.assertEqual(self.filler.db_define_ref.mock_calls[1], call('Users', keys, values))
        keys, values = ['contest_ref', 'problem_id'], [1, 'problem_id1']
        self.assertEqual(self.filler.db_define_ref.mock_calls[2], call('Problems', keys, values))
        keys, values = ['submit_id', 'problem_ref'], ['submit_id', 3]
        self.assertEqual(self.filler.db_define_ref.mock_calls[3], call('Submits', keys, values))
        keys, values = ['problem_ref', 'case_id'], [3, 'case_id0']
        self.assertEqual(self.filler.db_define_ref.mock_calls[4], call('Cases', keys, values))
        keys, values = ['submit_ref', 'case_ref'], [4, 5]
        self.assertEqual(self.filler.db_define_ref.mock_calls[5], call('Runs', keys, values))
        keys, values = ['problem_ref', 'case_id'], [3, 'case_id1']
        self.assertEqual(self.filler.db_define_ref.mock_calls[6], call('Cases', keys, values))
        keys, values = ['submit_ref', 'case_ref'], [4, 7]
        self.assertEqual(self.filler.db_define_ref.mock_calls[7], call('Runs', keys, values))

        self.assertEqual(len(self.filler.db_update.mock_calls), 3)
        keys, values = ['lang_id', 'outcome', 'timestamp', 'user_ref'], ['lang_id', 'outcome', 'timestamp', 2]
        self.assertEqual(self.filler.db_update.mock_calls[0], call('Submits', 4, keys, values))
        keys, values = ['realtime', 'time', 'outcome'], ['real_time0', 'time0', 'outcome0']
        self.assertEqual(self.filler.db_update.mock_calls[1], call('Runs', 6, keys, values))
        params = [('realtime', 'real_time1'), ('time', 'time1'), ('outcome', 'outcome1')]
        keys, values = ['realtime', 'time', 'outcome'], ['real_time1', 'time1', 'outcome1']
        self.assertEqual(self.filler.db_update.mock_calls[2], call('Runs', 8, keys, values))

    def test_define(self):
        self.filler.db_find_ref = Mock(return_value=1)
        self.assertEqual(self.filler.db_define_ref('table', ['one', 'two'], ['one_val', 'two_val']), 1)
        self.assertEqual(self.filler.db_cur.mock_calls, [])
        self.assertEqual(self.filler.db_find_ref.mock_calls, [call('table', ['one', 'two'], ['one_val', 'two_val'])])

    def test_define_none(self):
        self.filler.db_find_ref = Mock(side_effect=[None])
        self.filler.db_cur.lastrowid = 1
        keys, values = ['one', 'two'], ['one_val', 'two_val']
        self.assertEqual(self.filler.db_define_ref('table', keys, values), 1)
        params = ['INSERT INTO table (id, one, two) VALUES (NULL, ?, ?)', ['one_val', 'two_val']]
        self.assertEqual(self.filler.db_cur.mock_calls, [call.execute(*params)])
        self.assertEqual(self.filler.db_find_ref.mock_calls, [call('table', keys, values)])

    def test_find_right_values(self):
        self.filler.db_cur.fetchone.return_value = [1]
        self.assertEqual(self.filler.db_find_ref('table', ['one', 'two'], ['one_val', 'two_val']), 1)
        params = ['SELECT id FROM table WHERE one = ? AND two = ?', ['one_val', 'two_val']]
        self.assertEqual(self.filler.db_cur.mock_calls, [call.execute(*params), call.fetchone()])

    def test_find_none(self):
        self.filler.db_cur.fetchone.return_value = None
        self.assertEqual(self.filler.db_find_ref('', [], []), None)

    def test_update(self):
        self.filler.db_update('table', 1, ['one', 'two'], ['one_val', 'two_val'])
        params = ['UPDATE table SET one = ?, two = ? WHERE id = 1', ['one_val', 'two_val']]
        self.assertEqual(self.filler.db_cur.mock_calls, [call.execute(*params)])


if __name__ == "__main__":
    unittest.main()
