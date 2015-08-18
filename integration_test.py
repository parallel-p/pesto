from walker import PickleWorker, SubmitWalker
from ejudge_parse import ejudge_parse
from pickle_submits import PickleWriter
from visitor import FakeVisitor
import os.path
from shutil import rmtree
from unittest import main
from pesto_testcase import PestoTestCase


class IntegrationTest(PestoTestCase):
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
        self.pickler.default_path = os.path.join(self.temp_dir, 'integration_tests', 'pickle')

        try:
            os.makedirs(self.pickler.default_path)
        except FileExistsError:
            pass
        for submit in self.visitor.submits:
            self.pickler.visit(submit)
        self.pickler.close()

    def tearDown(self):
        if os.path.exists(self.pickler.default_path):
            rmtree(self.pickler.default_path)

    def test_preprocessing(self):
        walker = SubmitWalker(None)
        self.tested_submits = [submit for filename in
                                PickleWorker().walk(self.pickler.default_path) for submit in walker.walk(filename[1])]

        self.tested_submits = [''.join(map(str, submit.__dict__.values())) for submit in
                      self.tested_submits]

        self.visitor.submits = [''.join(map(str, submit.__dict__.values())) for submit in
                       self.visitor.submits]
        self.assertTrue(set(self.tested_submits) == set(self.visitor.submits))


if __name__ == '__main__':
    main()
