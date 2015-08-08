import mysql.connector

class MySQLConnector():
    def __init__(self):
        self.connector = mysql.connector
        self.connection = None

    def create_connection(self, config):
        self.config = config
        if self.connector.connection_id != None:
            self.connection.close()
        self.connection = self.connector.connect(**self.config)
        # NO ERRORS ARE CAUGHT HERE

    def get_cursor(self):
        if self.connection != None:
            return self.connection.cursor()

    def close(self):
        if self.connection != None:
            self.connection.close()
