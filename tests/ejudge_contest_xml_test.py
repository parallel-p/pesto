import unittest
from unittest.mock import patch, mock_open

from ejudge_contest_xml import ejudge_get_contest_name


class TextGetName(unittest.TestCase):
    @patch('builtins.open', mock_open(read_data='<contest><name>contestname</name></contest>'))
    def test_common(self):
        self.assertEqual(ejudge_get_contest_name('nope'), 'contestname')

    @patch('builtins.open', mock_open(read_data='<contest><noname>contestname</noname></contest>'))
    def test_no_name(self):
        self.assertIsNone(ejudge_get_contest_name('nope'))

    @patch('builtins.open', mock_open(read_data='not_xml'))
    def test_not_xml(self):
        self.assertIsNone(ejudge_get_contest_name('nope'))

    @patch('builtins.open', side_effect=UnicodeError)
    def test_not_utf8(self, op):
        self.assertIsNone(ejudge_get_contest_name('nope'))


if __name__ == "__main__":
    unittest.main()
