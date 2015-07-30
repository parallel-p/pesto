from memory_database import MemoryDatabase
import unittest


def parse(dirs, csv):
    return (dirs[0], csv)

class MemoryDatabaseTest(unittest.TestCase):
    def test_path(self):
        db = MemoryDatabase('dir', 'csv', parse)
        self.assertEqual(db.problems, 'dir')
        self.assertEqual(db.submits, 'csv')

    def test_strip(self):
        db = MemoryDatabase('dir\\', 'csv', parse)
        self.assertEqual(db.problems, 'dir')
        self.assertEqual(db.submits, 'csv')
        db = MemoryDatabase('dir/', 'csv', parse)
        self.assertEqual(db.problems, 'dir')
        self.assertEqual(db.submits, 'csv')
        db = MemoryDatabase('/dir/dir2', 'csv', parse)
        self.assertEqual(db.problems, '/dir/dir2')
        self.assertEqual(db.submits, 'csv')

if __name__ == "__main__":
    unittest.main()
