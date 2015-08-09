import mysql.connector

class MySQLConnector():
    def __init__(self):
        self.connector = mysql.connector
        self.connection = self.connector.connect()

    def create_connection(self, config):
        self.config = config
        if self.connection.is_connected():
            self.connection.close()
        self.connection = self.connector.connect(**self.config)

    def get_cursor(self):
        if self.connection.is_connected():
            return self.connection.cursor()

    def close(self):
        if self.connection.is_connected():
            self.connection.close()
