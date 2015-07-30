import os.path
import unittest
from ejudge_parse import ejudge_parse


def do_parse(version, contest):
    return ejudge_parse([os.path.join('testdata', 'memory_database', version, contest)], os.path.join('testdata', 'memory_database', version, 'db.csv'))


class TestEjudgeParser(unittest.TestCase):
    def test_good(self):
        problems, submits = do_parse('good', '001')
        self.assertEqual(len(submits), 8)
        self.assertEqual(len(problems), 4)

    def test_bad_csv(self):
        with self.assertRaises(ValueError):
            do_parse('csv', '001')

    def test_bad_xml(self):
        problems, submits = do_parse('xml', '001')
        self.assertEqual(len(submits), 7)
        self.assertEqual(len(problems), 4)

    def test_bad_gz(self):
        problems, submits = do_parse('gz', '001')
        self.assertEqual(len(submits), 7)
        self.assertEqual(len(problems), 3)

    def test_empty_folders(self):
        problems, submits = do_parse('empty_folders', '001')
        self.assertEqual(len(submits), 6)
        self.assertEqual(len(problems), 3)

    def test_name_zeros(self):
        problems, submits = do_parse('name_zeros', '00name')
        self.assertEqual(len(problems), 4)
        self.assertEqual(list(problems)[0][0], '00name')

    def test_digit_zeros(self):
        problems, submits = do_parse('digit_zeros', '0010')
        self.assertEqual(len(problems), 4)
        self.assertEqual(list(problems)[0][0], '10')

if __name__ == '__main__':
    unittest.main()