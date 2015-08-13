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
        return self.load(row)

    def define(self, origin, user_id):
        ref = self.lookup(origin, user_id)
        if ref is None:
            ref = self.create(origin, user_id)
        return ref

    def lookup(self, origin, user_id):
        cursor = self.connector.get_cursor()
        cursor.execute('SELECT id FROM Users WHERE origin = ? AND user_id = ?', [origin, user_id])
        response = cursor.fetchone()
        return response['id'] if response else None

    def create(self, origin, user_id):
        cursor = self.connector.get_cursor()
        cursor.execute('INSERT INTO Users (id, origin, user_id) VALUES (NULL, ?, ?)', [origin, user_id])
        return cursor.lastrowid

    def update(self, ref, update_def):
        cursor = self.connector.get_cursor()
        cursor.execute('SELECT {} FROM Users WHERE id = ?'.format(self.columns), [ref])
        old = self.load(cursor.fetchone())
        new_def = {'origin': old.origin, 'user_id': old.user_id}
        for key, value in update_def.items():
            new_def[key] = value
        new_def['id'] = ref
        cursor.execute('UPDATE Users SET origin = :origin, user_id = :user_id WHERE id = :id', new_def)
