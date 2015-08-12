import unittest
from unittest.mock import Mock
from pesto_testcase import PestoTestCase
from dao_runs import DAORuns
from model import Run


class RunsDaoTest(PestoTestCase):
    def setUp(self):
        self.cursor = Mock()
        self.row = ('id', 'submit_ref', 'real_time', 'time', 'outcome', 'case_ref')

    def test_load(self):
        arg = {'realtime':'realtime', 'time':'time', 'outcome':'outcome'}
        result = DAORuns.load(arg)
        run = Run('', '', '', 'realtime', 'time', 'outcome')
        self.assertEqual(result.real_time, run.real_time)
        self.assertEqual(result.time, run.time)
        self.assertEqual(result.outcome, run.outcome)

    def test_deep_load(self):
        conn = Mock()
        curs = Mock()
        curs.fetchone = Mock(return_value=('case_id', ''))
        conn.get_cursor.return_value = curs

        arg = {'realtime':'realtime', 'time':'time', 'outcome':'outcome', 'case_ref':'case_ref'}
        result = DAORuns(conn).deep_load(arg)

        run = Run(None, None, 'case_id', 'realtime', 'time', 'outcome')
        self.assertEqual(result.real_time, run.real_time)
        self.assertEqual(result.time, run.time)
        self.assertEqual(result.outcome, run.outcome)