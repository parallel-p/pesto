from db_submits_filler import DBSubmitsFiller
import unittest
from unittest.mock import Mock, call


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
        params = [('origin', 'origin'), ('scoring', 'scoring'), ('contest_id', 'problem_id0')]
        self.assertEqual(self.filler.db_define_ref.mock_calls[0], call('Contests', params))
        params = [('origin', 'origin'), ('user_id', 'user_id')]
        self.assertEqual(self.filler.db_define_ref.mock_calls[1], call('Users', params))
        params = [('contest_ref', 1), ('problem_id', 'problem_id1')]
        self.assertEqual(self.filler.db_define_ref.mock_calls[2], call('Problems', params))
        params = [('submit_id', 'submit_id'), ('problem', 3)]
        self.assertEqual(self.filler.db_define_ref.mock_calls[3], call('Submits', params))
        params = [('problem_ref', 3), ('case_id', 'case_id0')]
        self.assertEqual(self.filler.db_define_ref.mock_calls[4], call('Cases', params))
        params = [('submit_ref', 4), ('case_ref', 5)]
        self.assertEqual(self.filler.db_define_ref.mock_calls[5], call('Runs', params))
        params = [('problem_ref', 3), ('case_id', 'case_id1')]
        self.assertEqual(self.filler.db_define_ref.mock_calls[6], call('Cases', params))
        params = [('submit_ref', 4), ('case_ref', 7)]
        self.assertEqual(self.filler.db_define_ref.mock_calls[7], call('Runs', params))

        self.assertEqual(len(self.filler.db_update.mock_calls), 3)
        params = [('lang_id', 'lang_id'), ('outcome', 'outcome'), ('timestamp', 'timestamp'), ('user_ref', 2)]
        self.assertEqual(self.filler.db_update.mock_calls[0], call('Submits', 4, params))
        params = [('realtime', 'real_time0'), ('time', 'time0'), ('outcome', 'outcome0')]
        self.assertEqual(self.filler.db_update.mock_calls[1], call('Runs', 6, params))
        params = [('realtime', 'real_time1'), ('time', 'time1'), ('outcome', 'outcome1')]
        self.assertEqual(self.filler.db_update.mock_calls[2], call('Runs', 8, params))

    def test_define(self):
        self.filler.db_find_ref = Mock(return_value=1)
        self.assertEqual(self.filler.db_define_ref('table', [('one', 'one_val'), ('two', 'two_val')]), 1)
        self.assertEqual(self.filler.db_cur.mock_calls, [])
        self.assertEqual(self.filler.db_find_ref.mock_calls, [call('table', [('one', 'one_val'), ('two', 'two_val')])])

    def test_define_none(self):
        self.filler.db_find_ref = Mock(side_effect=[None, 1])
        def_params = [('one', 'one_val'), ('two', 'two_val')]
        self.assertEqual(self.filler.db_define_ref('table', def_params), 1)
        params = ['INSERT INTO table (id, ?, ?) VALUES (NULL, ?, ?)', 'one', 'two', 'one_val', 'two_val']
        self.assertEqual(self.filler.db_cur.mock_calls, [call.execute(*params)])
        self.assertEqual(self.filler.db_find_ref.mock_calls, [call('table', def_params)] * 2)

    def test_find_right_values(self):
        self.filler.db_cur.fetchone.return_value = [1]
        self.assertEqual(self.filler.db_find_ref('table', [('one', 'one_val'), ('two', 'two_val')]), 1)
        params = ['SELECT id FROM table WHERE ? = ? AND ? = ?', 'one', 'one_val', 'two', 'two_val']
        self.assertEqual(self.filler.db_cur.mock_calls, [call.execute(*params), call.fetchone()])

    def test_find_none(self):
        self.filler.db_cur.fetchone.return_value = None
        self.assertEqual(self.filler.db_find_ref('', []), None)

    def test_update(self):
        self.filler.db_update('table', 1, [('one', 'one_val'), ('two', 'two_val')])
        params = ['UPDATE table SET ? = ?, ? = ? WHERE id = ?', 'one', 'one_val', 'two', 'two_val', 1]
        self.assertEqual(self.filler.db_cur.mock_calls, [call.execute(*params)])

if __name__ == "__main__":
    unittest.main()
