import unittest
from unittest.mock import Mock, patch

from ejudge_database import EjudgeDatabase, EjudgeSubmitInfo


class TestEjudgeDatabase(unittest.TestCase):
    def test_submit_info(self):
        info = EjudgeSubmitInfo('1', '2', '3', 4)
        self.assertEqual(info.problem_id, '1')
        self.assertEqual(info.user_id, '2')
        self.assertEqual(info.lang_id, '3')
        self.assertEqual(info.timestamp, 4)

    def test_init(self):
        db = EjudgeDatabase('c')
        self.assertEqual(db.db_cursor, 'c')
        self.assertFalse(db.data)

    def test_get_info(self):
        db = EjudgeDatabase(Mock(fetchone=Mock(return_value=['1', '2', '3', 4])))
        info = db.get_submit_info('ci', 'si')
        db.db_cursor.execute.assert_called_once_with('SELECT prob_id,user_id,lang_id,create_time '
                                                     'FROM ejudge.runs WHERE contest_id=%(contest)s AND run_id=%(submit)s',
                                                     {'contest': 'ci', 'submit': 'si'})
        self.assertEqual(info.problem_id, '1')
        self.assertEqual(info.user_id, '2')
        self.assertEqual(info.lang_id, '3')
        self.assertEqual(info.timestamp, 4)

    @patch('logging.warning')
    def test_empty_response(self, warn):
        db = EjudgeDatabase(Mock(fetchone=Mock(return_value=None)))
        info = db.get_submit_info('ci', 'si')
        self.assertIsNone(info)
        self.assertTrue(warn.called)


if __name__ == "__main__":
    unittest.main()
