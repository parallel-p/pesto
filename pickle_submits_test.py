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
        submit = Submit(0, 0, 179, [], 1)

        submit.problem_id = ("17", "0")
        for i in range(100):
            self.pickle_submit.visit(submit)
        self.assertTrue(exists(join(".", "pickle", submit.problem_id[0])))
        
        submit.problem_id = ("18", "0")
        for i in range(100):
            self.pickle_submit.visit(submit)
        self.assertTrue(exists(join(".", "pickle", submit.problem_id[0])))


    def test_mk_many_pickles(self):
        submit = Submit(0, 0, 179, [], 1)
        submit.problem_id = ("17", "0")
        for i in range(10000):
            self.pickle_submit.visit(submit)
        self.assertEqual(len(listdir(join(".", "pickle", submit.problem_id[0]))), 100)

if __name__ == "__main__":
    unittest.main()
