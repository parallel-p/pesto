import unittest
from unittest.mock import patch, mock_open

from ejudge_contest_xml import ejudge_get_contest_name


class TextGetName(unittest.TestCase):
    @patch('builtins.open', mock_open(read_data='<contest><name>contestname</name></contest>'))
    def test_common(self):
        self.assertEqual(ejudge_get_contest_name('nope'), 'contestname')

    @patch('builtins.open', mock_open(read_data='<contest><noname>contestname</noname></contest>'))
    @patch('logging.error')
    def test_no_name(self, err):
        self.assertIsNone(ejudge_get_contest_name('nope'))
        self.assertTrue(err.called)

    @patch('builtins.open', mock_open(read_data='not_xml'))
    @patch('logging.error')
    def test_not_xml(self, err):
        self.assertIsNone(ejudge_get_contest_name('nope'))
        self.assertTrue(err.called)

    @patch('builtins.open', side_effect=UnicodeError)
    @patch('logging.error')
    def test_not_utf8(self, op, err):
        self.assertIsNone(ejudge_get_contest_name('nope'))
        self.assertTrue(err.called)

if __name__ == "__main__":
    unittest.main()
