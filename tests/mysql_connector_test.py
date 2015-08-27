import unittest
from unittest.mock import Mock, patch

from mysql_connector import MySQLConnector


class MySQLConnTest(unittest.TestCase):
    @patch('mysql.connector')
    def test_init(self, mc):
        conn = MySQLConnector()
        mc.connect.assert_any_call()

    @patch('mysql.connector')
    def test_create_connection(self, mc):
        conn = MySQLConnector()
        conn.close = Mock()
        conn.create_connection({'a': 1, 'b': 2})
        conn.close.assert_any_call()
        mc.connect.assert_called_with(a=1, b=2)

    @patch('mysql.connector')
    def test_get_cursor(self, mc):
        conn = MySQLConnector()
        conn.connection.is_connected = Mock(return_value=True)
        conn.connection.cursor.return_value = 42
        self.assertEqual(conn.get_cursor(), 42)
        conn.connection.is_connected.return_value = False
        self.assertIsNone(conn.get_cursor())

    @patch('mysql.connector')
    def test_close(self, mc):
        conn = MySQLConnector()
        conn.connection.is_connected = Mock(return_value=False)
        conn.close()
        self.assertFalse(conn.connection.close.mock_calls)
        conn.connection.is_connected.return_value = True
        conn.close()
        conn.connection.close.assert_any_call()


if __name__ == "__main__":
    unittest.main()
