import unittest
import os.path
from ejudgedb import EjudgeDB, EjudgeDBEntry


def make_path(csv_filename):
    return os.path.join('testdata', 'ejudgedb', csv_filename)


class TestEjudgeDB(unittest.TestCase):

    def test_ejudgedb_init(self):
        db = EjudgeDB(make_path('good.csv'))
        self.assertEqual(len(db.data), 6)

    def test_empty_lines(self):
        db = EjudgeDB(make_path('good_empty_lines.csv'))
        self.assertEqual(len(db.data), 6)

    def test_bad_csv(self):
        with self.assertRaises(Exception):
            EjudgeDB(make_path('bad.csv'))

    def test_contest_ids(self):
        db = EjudgeDB(make_path('good.csv'), contest_ids=["42", "43"])
        self.assertEqual(len(db.data), 6)
        db = EjudgeDB(make_path('good.csv'), contest_ids=["11"])
        self.assertEqual(len(db.data), 0)

    def test_get_problem_id(self):
        db = EjudgeDB(make_path('good.csv'))
        self.assertEqual(db.get_problem_id("42", "2"), "2")
        self.assertEqual(db.get_problem_id("41", "2"), None)
        self.assertEqual(db.get_problem_id("42", "7"), None)

    def test_get_user_id(self):
        db = EjudgeDB(make_path('good.csv'))
        self.assertEqual(db.get_user_id("42", "1"), "228")
        self.assertEqual(db.get_user_id("41", "2"), None)
        self.assertEqual(db.get_user_id("42", "7"), None)

    def test_get_lang_id(self):
        db = EjudgeDB(make_path('good.csv'))
        self.assertEqual(db.get_lang_id("42", "1"), "2")
        self.assertEqual(db.get_lang_id("41", "2"), None)
        self.assertEqual(db.get_lang_id("42", "7"), None)

    def test_db_entry(self):
        entry = EjudgeDBEntry("1", "2", "3")
        self.assertEqual(entry.problem_id, "1")
        self.assertEqual(entry.user_id, "2")
        self.assertEqual(entry.lang_id, "3")

if __name__ == "__main__":
    unittest.main()
