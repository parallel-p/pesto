from fill_db_from_submit import fill_db_from_submit
from fill_db_from_submit import db_define_ref
from fill_db_from_submit import db_find_ref
from fill_db_from_submit import db_update
import fill_db_from_submit as db
import unittest
from unittest.mock import Mock, call


class TestFillDBFromSubmit(unittest.TestCase):
    def setUp(self):
        self.db_cur = Mock()

    def test_right_values(self):
        db.db_define_ref = Mock(side_effect=[1, 2, 3, 4, 5, 6, 7, 8])
        db.db_update = Mock()
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
        fill_db_from_submit(self.db_cur, submit, 'origin')
        self.assertEqual(len(db.db_define_ref.mock_calls), 8)
        params = [('origin', 'origin'), ('scoring', 'scoring'), ('contest_id', 'problem_id0')]
        self.assertEqual(db.db_define_ref.mock_calls[0], call(self.db_cur, 'Contests', params))
        params = [('origin', 'origin'), ('user_id', 'user_id')]
        self.assertEqual(db.db_define_ref.mock_calls[1], call(self.db_cur, 'Users', params))
        params = [('contest_ref', 1), ('problem_id', 'problem_id1')]
        self.assertEqual(db.db_define_ref.mock_calls[2], call(self.db_cur, 'Problems', params))
        params = [('submit_id', 'submit_id'), ('problem', 3)]
        self.assertEqual(db.db_define_ref.mock_calls[3], call(self.db_cur, 'Submits', params))
        params = [('problem_ref', 3), ('case_id', 'case_id0')]
        self.assertEqual(db.db_define_ref.mock_calls[4], call(self.db_cur, 'Cases', params))
        params = [('submit_ref', 4), ('case_ref', 5)]
        self.assertEqual(db.db_define_ref.mock_calls[5], call(self.db_cur, 'Runs', params))
        params = [('problem_ref', 3), ('case_id', 'case_id1')]
        self.assertEqual(db.db_define_ref.mock_calls[6], call(self.db_cur, 'Cases', params))
        params = [('submit_ref', 4), ('case_ref', 7)]
        self.assertEqual(db.db_define_ref.mock_calls[7], call(self.db_cur, 'Runs', params))

        self.assertEqual(len(db.db_update.mock_calls), 3)
        params = [('lang_id', 'lang_id'), ('outcome', 'outcome'), ('timestamp', 'timestamp'), ('user_ref', 2)]
        self.assertEqual(db.db_update.mock_calls[0], call(self.db_cur, 'Submits', 4, params))
        params = [('realtime', 'real_time0'), ('time', 'time0'), ('outcome', 'outcome0')]
        self.assertEqual(db.db_update.mock_calls[1], call(self.db_cur, 'Runs', 6, params))
        params = [('realtime', 'real_time1'), ('time', 'time1'), ('outcome', 'outcome1')]
        self.assertEqual(db.db_update.mock_calls[2], call(self.db_cur, 'Runs', 8, params))

    def test_define(self):
        db.db_find_ref = Mock(return_value=1)
        self.assertEqual(db_define_ref(self.db_cur, 'table', [('one', 'one_val'), ('two', 'two_val')]), 1)
        self.assertEqual(self.db_cur.mock_calls, [])
        self.assertEqual(db.db_find_ref.mock_calls, [call(self.db_cur, 'table', [('one', 'one_val'), ('two', 'two_val')])])

    def test_define_none(self):
        db.db_find_ref = Mock(side_effect=[None, 1])
        def_params = [('one', 'one_val'), ('two', 'two_val')]
        self.assertEqual(db_define_ref(self.db_cur, 'table', def_params), 1)
        params = ['INSERT INTO table (id, ?, ?) VALUES (NULL, ?, ?)', 'one', 'two', 'one_val', 'two_val']
        self.assertEqual(self.db_cur.mock_calls, [call.execute(*params)])
        self.assertEqual(db.db_find_ref.mock_calls, [call(self.db_cur, 'table', def_params)] * 2)

    def test_find_right_values(self):
        self.db_cur.fetchone.return_value = [1]
        self.assertEqual(db_find_ref(self.db_cur, 'table', [('one', 'one_val'), ('two', 'two_val')]), 1)
        params = ['SELECT id FROM table WHERE ? = ? AND ? = ?', 'one', 'one_val', 'two', 'two_val']
        self.assertEqual(self.db_cur.mock_calls, [call.execute(*params), call.fetchone()])

    def test_find_none(self):
        self.db_cur.fetchone.return_value = None
        self.assertEqual(db_find_ref(self.db_cur, '', []), None)

    def test_update(self):
        db_update(self.db_cur, 'table', 1, [('one', 'one_val'), ('two', 'two_val')])
        params = ['UPDATE table SET ? = ?, ? = ? WHERE id = ?', 'one', 'one_val', 'two', 'two_val', 1]
        self.assertEqual(self.db_cur.mock_calls, [call.execute(*params)])

if __name__ == "__main__":
    unittest.main()
