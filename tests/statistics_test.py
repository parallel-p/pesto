import unittest
from unittest.mock import Mock, MagicMock, patch
from statistics import Statistics, SubmitStatistics, ProblemStatistics

class TestStatistics(unittest.TestCase):
    def test_init(self):
        s = Statistics('c', 'f', 'e')
        self.assertEqual(s.filters, 'f')
        self.assertEqual(s.extra, 'e')
        self.assertIsNone(s.result)

    def test_string(self):
        s = Statistics('c')
        s.result = 1
        self.assertEqual(s.as_string(), '1')

    @patch('builtins.open')
    @patch('builtins.print')
    def test_save(self, pr, op):
        s = Statistics('c')
        s.result = 1
        s.save_to_file('file')
        op.assert_called_once_with('file', 'w')
        op.return_value.__enter__.return_value.write.assert_called_once_with('1')
        s.save_to_file(None)
        pr.assert_called_once_with('1')

class TestSubmitStatistics(unittest.TestCase):
    @patch('statistics.SubmitStatistics.calc')
    @patch('dao.SubmitsDAO.columns', '_c_')
    def test_create_query(self, c):
        good = 'SELECT _c_, Contests.scoring, Contests.contest_id, Problems.problem_id FROM Submits JOIN Problems ON Submits.problem_ref=Problems.id JOIN Contests ON Problems.contest_ref = CONTESTS.id'
        s = SubmitStatistics(Mock())
        self.assertEqual(s._create_query(), (good, []))
        s.filters = {'scoring':'sc', 'problem':'pr'}
        self.assertEqual(s._create_query(), (good + ' WHERE Contests.scoring = ? AND Problems.problem_id = ?', ['sc', 'pr']))
        s.filters = {'contest':'c'}
        self.assertEqual(s._create_query(), (good + ' WHERE Contests.contest_id = ?', ['c']))

    @patch('statistics.SubmitStatistics.calc')
    @patch('dao.SubmitsDAO')
    def test_get_data(self, dao, c):
        conn = Mock()
        s = SubmitStatistics(conn)
        s._create_query = Mock(return_value=('query {}', ('val',)))
        dao.return_value.deep_load = lambda *p:p
        conn.get_cursor.return_value.execute.return_value = [(10, 11, 12), (20, 21, 22)]
        self.assertEqual(list(s.get_input_data(conn)), [((10, 11, 12), (11, 12), 10), ((20, 21, 22), (21, 22), 20)])
        conn.get_cursor.return_value.execute.assert_called_with('query {}', ('val',))

    def test_calc(self):
        s = SubmitStatistics(MagicMock())
        s._create_visitor()
        vis = Mock()
        s._create_visitor = Mock(return_value=vis)
        s.calc([1, 2])
        self.assertEqual(s.result, vis)
        vis.visit.assert_any_call(1)
        vis.visit.assert_any_call(2)

    def test_string(self):
        s = SubmitStatistics(MagicMock())
        s.result = Mock(pretty_print=Mock(return_value='pp'))
        self.assertEqual(s.as_string(), 'pp')

class TestProblemStatistics(unittest.TestCase):
    @patch('statistics.ProblemStatistics.calc')
    @patch('dao.ProblemsDAO.columns', '_c_')
    def test_create_query(self, c):
        good = 'SELECT _c_, Contests.contest_id FROM Problems JOIN Contests ON Problems.contest_ref = Contests.id'
        s = ProblemStatistics(Mock())
        self.assertEqual(s._create_query(), (good, []))
        s.filters = {'scoring':'sc', 'problem':'pr'}
        self.assertEqual(s._create_query(), (good + ' WHERE Contests.scoring = ? AND Problems.problem_id = ?', ['sc', 'pr']))
        s.filters = {'contest':'c'}
        self.assertEqual(s._create_query(), (good + ' WHERE Contests.contest_id = ?', ['c']))

    @patch('statistics.ProblemStatistics.calc')
    @patch('dao.ProblemsDAO')
    def test_get_data(self, dao, c):
        conn = Mock()
        s = ProblemStatistics(conn)
        s._create_query = Mock(return_value=('query {}', ('val',)))
        dao.return_value.deep_load = lambda *p:p
        conn.get_cursor.return_value.execute.return_value = [{'contest_id':'1', 'a':'b'}, {'contest_id':'2'}]
        self.assertEqual(list(s.get_input_data(conn)), [({'contest_id': '1', 'a':'b'}, '1'), ({'contest_id': '2'}, '2')])
        conn.get_cursor.return_value.execute.assert_called_with('query {}', ('val',))

    @patch('statistics.ProblemStatistics.counter_class')
    def test_calc(self, cc):
        s = ProblemStatistics(MagicMock())
        s.calc('a')
        cc.asseet_called_once_with('a')


if __name__ == '__main__':
    unittest.main()
