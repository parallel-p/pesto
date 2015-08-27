import unittest
import sqlite3
from unittest.mock import MagicMock, patch

from sqlite_connector import SQLiteConnector
import pesto_testcase


class SQLiteConnectorTest(pesto_testcase.PestoTestCase):
    def setUp(self):
        self.connector = SQLiteConnector()

    @patch('sqlite3.connect', MagicMock())
    def test_connection(self):
        self.connector.create_connection('test_database')
        sqlite3.connect.assert_called_with('test_database')
        sqlite3.connect.return_value.cursor.return_value = 69
        self.assertEqual(self.connector.get_cursor(), 69)

    @patch('sqlite3.connect', MagicMock())
    def test_get_cursor(self):
        self.connector.create_connection('test_database')
        sqlite3.connect.cursor.assert_called_once()

    @patch('sqlite3.connect', MagicMock())
    def test_close_connection(self):
        self.connector.create_connection('test_database')
        self.connector.close_connection()
        sqlite3.connect.commit.assert_called_once()
        sqlite3.connect.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
