import os.path
import unittest
from visitor import Visitor
from ejudge_parse import ejudge_parse


class FakeVisitor(Visitor):
    def __init__(self):
        super().__init__()
        self.submits = 0
        self.submit_list = []

    def update_submit(self, submit):
        self.submits += 1
        self.submit_list.append(submit)


def do_parse(version, contest, visitor):
    contest_dirs = [os.path.join('testdata', 'memory_database', version, contest)]
    csv_filename = os.path.join('testdata', 'memory_database', version, 'db.csv')
    ejudge_parse(contest_dirs, csv_filename, visitor)


class TestEjudgeParser(unittest.TestCase):
    def setUp(self):
        self.visitor = FakeVisitor()

    def test_good(self):
        do_parse('good', '001', self.visitor)
        self.assertEqual(self.visitor.submits, 8)

    def test_trailing_slash(self):
        do_parse('good', '001/', self.visitor)
        self.assertEqual(self.visitor.submits, 8)

    def test_trailing_backslash(self):
        do_parse('good', '001\\', self.visitor)
        self.assertEqual(self.visitor.submits, 8)

    def test_bad_csv(self):
        with self.assertRaises(ValueError):
            do_parse('csv', '001', self.visitor)

    def test_bad_xml(self):
        do_parse('xml', '001', self.visitor)
        self.assertEqual(self.visitor.submits, 7)

    def test_bad_gz(self):
        do_parse('gz', '001', self.visitor)
        self.assertEqual(self.visitor.submits, 7)

    def test_empty_folders(self):
        do_parse('empty_folders', '001', self.visitor)
        self.assertEqual(self.visitor.submits, 6)

    def test_name_zeros(self):
        do_parse('name_zeros', '00name', self.visitor)
        self.assertEqual(self.visitor.submits, 8)

    def test_digit_zeros(self):
        do_parse('digit_zeros', '0010', self.visitor)
        self.assertEqual(self.visitor.submits, 8)

    def test_run_number(self):
        do_parse('digit_zeros', '0010', self.visitor)
        self.assertEqual(self.visitor.submit_list[0].runs[0].case_id, 1)

    def test_double_contest(self):
        contest_dirs = list()
        contest_dirs.append(os.path.join('testdata', 'memory_database', 'good', '001'))
        contest_dirs.append(os.path.join('testdata', 'memory_database', 'gz', '001'))
        csv_filename = os.path.join('testdata', 'memory_database', 'good', 'db.csv')
        ejudge_parse(contest_dirs, csv_filename, self.visitor)
        self.assertEqual(self.visitor.submits, 15)

if __name__ == '__main__':
    unittest.main()
