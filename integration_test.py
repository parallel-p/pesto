from pickle_walker import pickle_walker
from ejudge_parse import ejudge_parse
from pickle_submits import PickleWriter
from visitor import FakeVisitor
import os.path
from shutil import rmtree
from unittest import TestCase, main


class IntegrationTest(TestCase):
    def setUp(self):
        self.visitor = FakeVisitor()
        contest_dir = [os.path.join('.', '', 'contests',
                                    '000017'),
                       os.path.join('testdata', 'integration_tests', 'contests',
                                    '000018')]
        csv_dir = os.path.join('testdata', 'integration_tests',
                               'multiple_submits_count_submit_test.csv')
        ejudge_parse(contest_dir, csv_dir, self.visitor)
        self.pickler = PickleWriter()
        self.pickler.default_path = os.path.join('.', 'testdata', 'integration_tests',
                                                 'pickle')
        for submit in self.visitor.submits:
            self.pickler.visit(submit)
        self.pickler.close()

    def tearDown(self):
        if os.path.exists(self.pickler.default_path):
            rmtree(self.pickler.default_path)

    def test_preprocessing(self):
        self.tested_submits = [submit for submit in
                                pickle_walker(self.pickler.default_path)]

        self.tested_submits = [''.join(map(str, submit.__dict__.values())) for submit in
                      self.tested_submits]

        self.visitor.submits = [''.join(map(str, submit.__dict__.values())) for submit in
                       self.visitor.submits]
        self.assertTrue(set(self.tested_submits) == set(self.visitor.submits))


if __name__ == '__main__':
    main()
