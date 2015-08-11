from model import User


class DAOUsers:
    columns = 'origin, user_id'

    def __init__(self, connector):
        self.connector = connector

    @staticmethod
    def load(row):
        result = User(row['user_id'], row['origin'])
        return result

    def deep_load(self, row):
        return DAOUsers.load(row)
