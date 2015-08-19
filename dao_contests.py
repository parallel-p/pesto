import model


class DAOContests:
    columns = 'contest_id, origin, name, scoring'

    def __init__(self, connector):
        self.connector = connector

    @staticmethod
    def load(row):
        result = model.Contest(row['contest_id'], row['origin'], row['name'], row['scoring'])
        return result

    def deep_load(self, row):
        return self.load(row)

    def define(self, origin, scoring, contest_id):
        ref = self.lookup(origin, scoring, contest_id)
        if ref is None:
            ref = self.create(origin, scoring, contest_id)
        return ref

    def lookup(self, origin, scoring, contest_id):
        cursor = self.connector.get_cursor()
        cursor.execute('SELECT id FROM Contests WHERE origin = ? AND scoring = ? AND contest_id = ?',
                       [origin, scoring, contest_id])
        response = cursor.fetchone()
        return response['id'] if response else None

    def create(self, origin, scoring, contest_id):
        cursor = self.connector.get_cursor()
        cursor.execute('INSERT INTO Contests (id, origin, scoring, contest_id) VALUES (NULL, ?, ?, ?)',
                       [origin, scoring, contest_id])
        return cursor.lastrowid

    def update(self, ref, update_def):
        cursor = self.connector.get_cursor()
        cursor.execute('SELECT {} FROM Contests WHERE id = ?'.format(DAOContests.columns), [ref])
        old = self.load(cursor.fetchone())
        new_def = {'origin': old.origin, 'name': old.name, 'scoring': old.scoring, 'contest_id': old.contest_id}
        for key, value in update_def.items():
            new_def[key] = value
        new_def['id'] = ref
        cursor.execute('UPDATE Contests SET origin = :origin, name = :name, scoring = :scoring, '
                       'contest_id = :contest_id WHERE id = :id', new_def)
