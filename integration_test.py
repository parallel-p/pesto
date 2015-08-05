from pickle_walker import pickle_walker
from ejudge_parse import ejudge_parse
from pickle_submits import PickleWriter
from visitor import FakeVisitor
import os.path
from os.path import exists, join
from shutil import rmtree


def main():
    visitor = FakeVisitor()
    contest_dir = [os.path.join('.', '', 'contests',
                                '000017'),
                   os.path.join('testdata', 'integration_tests', 'contests',
                                '000018')]
    csv_dir = os.path.join('testdata', 'integration_tests',
                           'multiple_submits_count_submit_test.csv')
    ejudge_parse(contest_dir, csv_dir, visitor)
    pickler = PickleWriter()
    for submit in visitor.submits:
        pickler.visit(submit)

    tested_submits = [submit for submit in pickle_walker(os.path.join('.', 'pickle'))]
    tested_submits = (''.join(map(str, submit.__dict__.values())) for submit in
                      tested_submits)
    visitor.submits = (''.join(map(str, submit.__dict__.values())) for submit in
                       visitor.submits)

    if exists(join(".", "pickle")):
            rmtree(join(".", "pickle"))

    if set(tested_submits) == set(visitor.submits):
        print("Test passed")
    else:
        print("Test failed")


if __name__ == '__main__':
    main()
