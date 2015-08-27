import unittest
from unittest.mock import Mock, patch

from md5_hasher import _md5_update, get_hash


class TestMD5Hasher(unittest.TestCase):
    @patch('builtins.open', return_value=Mock(read=Mock(return_value='contents'), __exit__=Mock(),
                                              __enter__=Mock(return_value=Mock(read=Mock(return_value='contents'),
                                                                               close=Mock()))))
    def test_update(self, d):
        md5 = Mock()
        _md5_update(md5, 'filename')
        open.assert_called_once_with('filename', 'rb')
        md5.update.assert_called_once_with('contents')

    @patch('md5_hasher._md5_update', lambda md5, name: md5.update(name))
    def test_get_hash(self):
        self.assertEqual(get_hash(b'123', b'456'), 'e10adc3949ba59abbe56e057f20f883e')  # md5('123456')


if __name__ == "__main__":
    unittest.main()
