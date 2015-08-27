import mysql.connector


class MySQLConnector():
    """Class that creates connection to MySQL DB.
    Input variable "config" should be a dict, and contain following
    fields:
    'name': username
    'password': password
    'host': The host name or IP address of the MySQL server
    'port': The TCP/IP port of the MySQL server. Must be an integer (Default = 3306)
    'database': The database name

    Example of config
    config = {'user': 'pesto', 'password': 'trusty_pass', 'host': '10.0.0.80', 'port': 3316, 'database': 'ejudge_sis'}

    Important notice - this class doesn't handle any errors of connection etc.
    You'll have to watch them by yourself, when you're using this class.
    """

    def __init__(self):
        self.connector = mysql.connector
        self.connection = self.connector.connect()

    def create_connection(self, config):
        self.config = config
        self.close()
        self.connection = self.connector.connect(**self.config)

    def get_cursor(self):
        if self.connection.is_connected():
            return self.connection.cursor()

    def close(self):
        if self.connection.is_connected():
            self.connection.close()
