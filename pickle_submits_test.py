import unittest
from unittest.mock import Mock
from pickle_submits import PickleWriter
from shutil import rmtree
from os import mkdir, listdir
from os.path import exists, join
from model import Submit
from pesto_testcase import PestoTestCase


class PickleSubmitTests(PestoTestCase):
    def setUp(self):
        self.pickle_submit = PickleWriter()
        self.pickle_submit.default_path = join(self.temp_dir, "pickle_walker_")

    def tearDown(self):
        if exists(self.pickle_submit.default_path):
            rmtree(self.pickle_submit.default_path)

    def test_no_write(self):
        self.pickle_submit.visit(Submit('0', ('17', '0'), '179', '0', [], '1', 'kirov', 37))
        self.pickle_submit.write_file()
        self.pickle_submit.write_file()
        self.assertEqual(len(listdir(join(self.pickle_submit.default_path, '17'))), 1)

    def test_mk_diff_dir(self):
        submit = Submit('0', '0', '179', '0', [], '1', 'kirov', 37)

        submit.problem_id = ("17", "0")
        for i in range(100):
            self.pickle_submit.visit(submit)
        self.assertTrue(exists(join(self.pickle_submit.default_path, submit.problem_id[0])))

        submit.problem_id = ("18", "0")
        for i in range(100):
            self.pickle_submit.visit(submit)
        self.assertTrue(exists(join(self.pickle_submit.default_path, submit.problem_id[0])))

    def test_mk_many_pickles(self):
        submit = Submit('0', '0', '179', '0', [], '1', 'kirov', 37)
        submit.problem_id = ("17", "0")
        for i in range(9000):
            self.pickle_submit.visit(submit)
        self.assertEqual(len(listdir(join(self.pickle_submit.default_path, submit.problem_id[0]))), 90)

    def test_particial_sumbits(self):
        submit = Submit('0', '0', '179', '0', [], '1', 'kirov', 37)
        submit.problem_id = ("17", "0")
        for i in range(103):
            self.pickle_submit.visit(submit)
        self.pickle_submit.write_file()
        self.assertEqual(len(listdir(join(self.pickle_submit.default_path, submit.problem_id[0]))), 2)
        self.assertTrue(exists(join(self.pickle_submit.default_path, submit.problem_id[0], "pickle000001.pickle")))
        self.assertTrue(exists(join(self.pickle_submit.default_path, submit.problem_id[0], "pickle000001_3.pickle")))


if __name__ == "__main__":
    unittest.main()
