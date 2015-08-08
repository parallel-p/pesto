import unittest
import sqlite3
from unittest.mock import MagicMock
from sqlite_connector import SQLiteConnector
import pesto_testcase


class SQLiteConnectorTest(pesto_testcase.PestoTestCase):
    def setUp(self):
        self.connector = SQLiteConnector()

    def test_connection(self):
        sqlite3.connect = MagicMock(return_value='connection succeeded')
        self.connector.create_connection('test_database')
        sqlite3.connect.assert_called_with('test_database')
        self.assertEqual(self.connector.sqlite_connection,'connection succeeded')

    def test_get_cursor(self):
        sqlite3.connect = MagicMock()
        sqlite3.connect.cursor = MagicMock()
        self.connector.create_connection('test_database')
        sqlite3.connect.cursor.assert_called_once()

    def test_close_connection(self):
        sqlite3.connect = MagicMock()
        self.connector.create_connection('test_database')
        self.connector.close_connection()
        sqlite3.connect.commit.assert_called_once()
        sqlite3.connect.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()