import unittest
from unittest.mock import Mock
from pickle_submits import PickleWriter
from shutil import rmtree
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
        submit = Submit('0', '0', '179', '0', [], '1', "ACM")
        submit.problem_id = ("17", "0")
        for i in range(103):
            self.pickle_submit.visit(submit)
        self.pickle_submit.write_file()
        for parsed_submit in pickle_walker(join("pickle")):
            self.assertEqual(str(submit), str(parsed_submit))

    def test_empty_dir(self):
        parsed_submits = [parsed_submit for parsed_submit in pickle_walker(join(".", "testdata", "pickle_walker"))]
        self.assertEqual(len(parsed_submits), 0)

    def test_many_contests(self):
        submit = Submit('0', '0', '179', '0', [], '1', "ACM")
        submit.problem_id = ("17", "0")
        for i in range(101):
            self.pickle_submit.visit(submit)
        submit = Submit('0', '0', '179', '0', [], '1', "ACM")
        submit.problem_id = ("18", "0")
        for i in range(103):
            self.pickle_submit.visit(submit)
        self.pickle_submit.write_file()
        parsed_submits = [parsed_submit for parsed_submit in pickle_walker(join(".", "pickle"))]
        self.assertEqual(len(parsed_submits), 204)
        self.assertEqual(parsed_submits[100].problem_id[0], "17")
        self.assertEqual(parsed_submits[101].problem_id[0], "18")

if __name__ == "__main__":
    unittest.main()
