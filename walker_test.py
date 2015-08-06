from pesto_testcase import PestoTestCase
from walker import MultipleContestWalker
from walker import SingleContestWalker
from walker import EjudgeRunsFilesWorker
from walker import AllFilesWalker
from walker import PickleWorker
from walker import SubmitWalker
from unittest.mock import Mock, patch
import unittest
import os.path


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
                         ('2', os.path.join('testdata', 'ejudge_contest', '000002'))]
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


if __name__ == "__main__":
    unittest.main()
