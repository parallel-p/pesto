from pesto_testcase import PestoTestCase
from walker import MultipleContestWalker
from walker import SingleContestWalker
from walker import EjudgeRunsFilesWorker
from walker import AllFilesWalker
from walker import PickleWorker
from walker import SubmitWalker
from unittest.mock import Mock, patch, MagicMock
import unittest
import os.path
import pickle


class TestSingleContestWalker(PestoTestCase):
    def test_walk(self):
        walker = SingleContestWalker()
        self.assertEqual(list(walker.walk('000017'))[0], ('17', '000017'))
        self.assertEqual(list(walker.walk('000017/'))[0], ('17', '000017'))
        self.assertEqual(list(walker.walk('000017\\'))[0], ('17', '000017'))


class TestMultiContestWalker(PestoTestCase):
    def setUp(self):
        self.walker = MultipleContestWalker()

    def test_walk(self):
        contests_dir = os.path.join('testdata', 'ejudge_contest')
        contests = list(self.walker.walk(contests_dir))
        true_contests = [('1', os.path.join('testdata', 'ejudge_contest', '000001')),
                         ('2', os.path.join('testdata', 'ejudge_contest', '000002')),
                         ('3', os.path.join('testdata', 'ejudge_contest',
                                            'there_is_a_contest_inside', '000003'))]
        self.assertEqual(sorted(contests), sorted(true_contests))


class TestEjudgeRunsFilesWorker(PestoTestCase):
    def setUp(self):
        self.worker = EjudgeRunsFilesWorker()
        self.os_walk_backup = os.walk

    def tearDown(self):
        os.walk = self.os_walk_backup

    def test_common(self):
        os.walk = Mock(return_value=[('a', ['b'], ['c', 'f.gz']), ('b', ['c'], ['d'])])
        self.assertEqual(list(self.worker.walk('a')), [('xml', os.path.join('a', 'c')),
                                                       ('gzip', os.path.join('a', 'f.gz')),
                                                       ('xml', os.path.join('b', 'd'))])

    def test_empty(self):
        os.walk = Mock(return_value=[])
        self.assertEqual(list(self.worker.walk('')), [])


class TestAllFilesWalker(PestoTestCase):
    def setUp(self):
        self.walker = AllFilesWalker()

    def test_walk(self):
        dir = os.path.join('testdata', 'count_submit_test', '000017')
        files = list(self.walker.walk(dir))
        good_files = [('xml', os.path.join('testdata', 'count_submit_test', '000017', '000077')),
                      ('xml', os.path.join('testdata', 'count_submit_test', '000017', '0', '000066')),
                      ('gzip',os.path.join('testdata', 'count_submit_test', '000017', 'A', '000068.gz'))]
        self.assertEqual(sorted(files), sorted(good_files))


class TestPickleWalker(PestoTestCase):
    def setUp(self):
        self.walker = PickleWorker()

    def test_walk(self):
        dir = os.path.join('testdata', 'pickle_walker')
        files = list(self.walker.walk(dir))
        good_files = [('pickle', os.path.join('testdata', 'pickle_walker', '17', 'pickle000001.pickle')),
                      ('pickle', os.path.join('testdata', 'pickle_walker', '17', 'pickle000001_1.pickle')),
                      ('pickle', os.path.join('testdata', 'pickle_walker', '18', 'pickle000001.pickle')),
                      ('pickle', os.path.join('testdata', 'pickle_walker', '18', 'pickle000001_3.pickle'))]
        self.assertEqual(sorted(files), sorted(good_files))


class TestSubmitWalker(PestoTestCase):

    def test_init(self):
        w = SubmitWalker('7')
        self.assertEqual(w.database, '7')
        self.assertEqual(w.contest_id, 0)

    @patch('builtins.open', return_value=MagicMock(__exit__=Mock(return_value=False)))
    @patch('pickle.load', return_value=[1, 2, 3])
    def test_submit_from_pickle(self, pk, op):
        res = list(SubmitWalker._get_submit_from_pickle(Mock(), 'filename'))
        op.assert_called_once_with('filename', 'rb')
        pk.asssert_called_once_with(42)
        self.assertEqual(res, [1, 2, 3])

    @patch('builtins.open', return_value=MagicMock(__exit__=Mock(return_value=False)))
    @patch('pickle.load', return_value=[1, 2, 3], side_effect=pickle.UnpicklingError())
    def test_submit_from_pickle_error(self, pk, op):
        res = list(SubmitWalker._get_submit_from_pickle(Mock(), 'filename'))
        op.assert_called_once_with('filename', 'rb')
        pk.asssert_called_once_with(42)
        self.assertEqual(res, [])

    @patch('walker.EjudgeDB', return_value=5)
    @patch('walker.ejudge_xml_parse', return_value=Mock(submit_id='5', submit_outcome='OK', scoring='ACM', run_outcomes=[('2', '3', 'OK'), ('4', '5', 'WA')]))
    def test_get_submit_from_xml(self, par, db):
        w = SubmitWalker('a')
        w.contest_id = '7'
        w.database = Mock()
        w.database.get_submit_info.return_value = Mock(problem_id='1', user_id='11', lang_id='2', timestamp=42)
        res = w._get_submit_from_xml('filename')
        self.assertEqual(res.submit_id, '5')
        self.assertEqual(res.problem_id, ('7', '1'))
        self.assertEqual(res.user_id, '11')
        self.assertEqual(res.lang_id, '2')
        self.assertEqual(res.outcome, 'OK')
        self.assertEqual(res.scoring, 'ACM')
        self.assertEqual(res.timestamp, 42)
        self.assertEqual((res.runs[0].problem_id, res.runs[0].submit_id, res.runs[0].case_id, res.runs[0].real_time,
                          res.runs[0].time, res.runs[0].outcome),
                         (('7', '1'), '5', 1, '2', '3', 'OK'))
        self.assertEqual((res.runs[1].problem_id, res.runs[1].submit_id, res.runs[1].case_id, res.runs[1].real_time,
                          res.runs[1].time, res.runs[1].outcome),
                         (('7', '1'), '5', 2, '4', '5', 'WA'))
        par.assert_called_once_with('filename')

    @patch('walker.EjudgeDB', return_value=5)
    @patch('walker.ejudge_xml_parse', return_value=None)
    def test_get_submit_from_xml_none(self, par, db):
        w = SubmitWalker('a')
        res = w._get_submit_from_xml('filename')
        self.assertIsNone(res)

    @patch('walker.EjudgeDB', return_value=5)
    @patch('walker.ejudge_xml_parse', return_value=None, side_effect=OSError())
    def test_get_submit_from_xml_error(self, par, db):
        w = SubmitWalker('a')
        res = w._get_submit_from_xml('filename')
        self.assertIsNone(res)


if __name__ == "__main__":
    unittest.main()
