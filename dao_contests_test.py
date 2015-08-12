import unittest
from unittest.mock import Mock
from dao_contests import DAOContests
import model


class DAOContestsTest(unittest.TestCase):
    def setUp(self):
        self.row = {'id': '1', 'contest_id': '42', 'origin': 'orig', 'name': 'Untitled', 'scoring': 'ACM'}
        self.dao = DAOContests(Mock())
        model.Contest = Mock(return_value='Contest_object')

    def test_load(self):
        return_value = self.dao.load(self.row)
        self.assertEqual(return_value, 'Contest_object')
        model.Contest.assert_called_once_with('42', 'orig', 'Untitled', 'ACM')

    def test_deep_load(self):
        return_value = self.dao.deep_load(self.row)
        self.assertEqual(return_value, 'Contest_object')
        model.Contest.assert_called_once_with('42', 'orig', 'Untitled', 'ACM')

if __name__ == "__main__":
    unittest.main()
