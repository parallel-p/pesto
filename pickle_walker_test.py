import unittest
from unittest.mock import Mock
from pickle_submits import PickleWriter
from shutil import rmtree
from os import mkdir, listdir
from os.path import exists, join
from model import Submit
from pickle_walker import pickle_walker



class Tester(unittest.TestCase):
    def setUp(self):
        self.pickle_submit = PickleWriter()

    def tearDown(self):
        if exists(join(".", "pickle")):
            rmtree(join(".", "pickle"))


    def test_mk_many_pickles(self):
        submit = Submit(0, 0, 179, 0, [], 1, 'ACM')
        submit.problem_id = ("17", "0")
        for i in range(3):
            self.pickle_submit.visit(submit)

        for i in pickle_walker('pickle/17'):
            self.assertEqual(submit, i)


if __name__ == "__main__":
    unittest.main()
