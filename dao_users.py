from model import User


class DAOUsers:
    def __init__(self, connector):
        self.connector = connector

    @staticmethod
    def load(row):
        result = User(row[2], row[1])
        return result

    def deep_load(self, row):
        return DAOUsers.load(row)