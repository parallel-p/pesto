import unittest
from unittest.mock import Mock
from pickle_submits import PickleWriter
from shutil import rmtree
from os import mkdir, listdir
from os.path import exists, join
from model import Submit


class PickleSubmitTests(unittest.TestCase):
    def setUp(self):
        self.pickle_submit = PickleWriter()

    def tearDown(self):
        if exists(join(".", "pickle")):
            rmtree(join(".", "pickle"))

    def test_mk_diff_dir(self):
        submit = Submit(0, 0, 179, 0, [], 1, 'ACM')

        submit.problem_id = ("17", "0")
        for i in range(100):
            self.pickle_submit.visit(submit)
        self.assertTrue(exists(join(".", "pickle", submit.problem_id[0])))

        submit.problem_id = ("18", "0")
        for i in range(100):
            self.pickle_submit.visit(submit)
        self.assertTrue(exists(join(".", "pickle", submit.problem_id[0])))

    def test_mk_many_pickles(self):
        submit = Submit(0, 0, 179, 0, [], 1, 'ACM')
        submit.problem_id = ("17", "0")
        for i in range(9000):
            self.pickle_submit.visit(submit)
        self.assertEqual(len(listdir(join(".", "pickle", submit.problem_id[0]))), 90)

    def test_particial_sumbits(self):
        submit = Submit(0, 0, 179, 0, [], 1, 'ACM')
        submit.problem_id = ("17", "0")
        for i in range(103):
            self.pickle_submit.visit(submit)
        self.pickle_submit.write_file()
        self.assertEqual(len(listdir(join(".", "pickle", submit.problem_id[0]))), 2)
        self.assertTrue(exists(join(".", "pickle", submit.problem_id[0], "pickle000001.pickle")))
        self.assertTrue(exists(join(".", "pickle", submit.problem_id[0], "pickle000001_3.pickle")))


if __name__ == "__main__":
    unittest.main()
