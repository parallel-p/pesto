import unittest
from unittest.mock import Mock
from pesto_testcase import PestoTestCase
from ejudge_runs_files_worker import EjudgeRunsFilesWorker
import os


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

if __name__ == "__main__":
    unittest.main()
