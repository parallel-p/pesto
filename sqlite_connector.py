import sqlite3


class SQLiteConnector:
    def __init__(self):
        self.sqlite_connection = None

    def create_connection(self, db_dir):
        self.sqlite_connection = sqlite3.connect(db_dir)

    def get_cursor(self):
        return self.sqlite_connection.cursor()

    def close_connection(self):
        self.sqlite_connection.commit()
        self.sqlite_connection.close()
