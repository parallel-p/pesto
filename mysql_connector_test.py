import unittest
from unittest.mock import Mock
from pesto_testcase import PestoTestCase
from mysql_connector import MySQLConnector

class MySQLConnTest(PestoTestCase):
    def setUp(self):
        self.connector = MySQLConnector()

    def test_connection(self):
        self.connector.create_connection = Mock()
        config = {'user': 'Scott', 'password': 'qwerty', 'host': '127.0.0.1', 'port': 8880, 'database': 'ejudge'}
        self.connector.create_connection(config)
        self.connector.create_connection.assert_called_once_with(config)

    def test_get_cursor(self):
        self.connector.get_cursor = Mock(return_value="Get this!")
        result = self.connector.get_cursor()
        self.connector.get_cursor.assert_called_once_with()
        self.assertEqual(result, "Get this!")

    def test_close(self):
        self.connector.close = Mock()
        self.connector.close()
        self.connector.close.assert_called_once_with()

if __name__ == "main":
    unittest.main()
