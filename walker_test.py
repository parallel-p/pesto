from pesto_testcase import PestoTestCase
from walker import MultipleContestWalker
from walker import EjudgeRunsFilesWorker
from unittest.mock import Mock
import os.path


class TestMultiContestWalker(PestoTestCase):
    def setUp(self):
        self.walker = MultipleContestWalker()

    def test_walk(self):
        contests_dir = os.path.join('testdata', 'ejudge_contest')
        contests = [contest for contest in self.walker.walk(contests_dir)]
        true_contests = [('1', os.path.join('testdata', 'ejudge_contest', '000001')),
                         ('2', os.path.join('testdata', 'ejudge_contest', '000002'))]
        self.assertEqual(sorted(contests), sorted(true_contests))

class EjudgeRunsFilesWorkerTest(PestoTestCase):
    def setUp(self):
        self.worker = EjudgeRunsFilesWorker()
        self.os_walk_backup = os.walk

    def tearDown(self):
        os.walk = self.os_walk_backup

    def test_common(self):
        os.walk = Mock(return_value=[('a', ['b'], ['c', 'f.gz']), ('b', ['c'], ['d'])])
        self.assertEqual(list(self.worker.walk('a')), [('xml', os.path.join('a', 'c')), ('gzip', os.path.join('a', 'f.gz')), ('xml', os.path.join('b', 'd'))])

    def test_empty(self):
        os.walk = Mock(return_value=[])
        self.assertEqual(list(self.worker.walk('')), [])