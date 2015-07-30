import unittest
from os.path import join
from traverse import traverse_contest

class PositiveTests(unittest.TestCase):
    def test_find_all_files(self):
        self.path = join('.', 'testdata', 'traverse')
        sample = set() # set of all files in test directory
        sample.add(join('.', 'testdata', 'traverse', '0', '0', 'second'))
        sample.add(join('.', 'testdata', 'traverse', '0', '1', '0', 'first'))
        sample.add(join('.', 'testdata', 'traverse', '0', '0', 'forth.gz'))
        sample.add(join('.', 'testdata', 'traverse', 'not_gz.gz'))
        sample.add(join('.', 'testdata', 'traverse', '0', '1', '1', 'third'))
        self.assertEqual(set([file.name for file in traverse_contest(self.path)]), sample)


if __name__ == "__main__":
    unittest.main() 