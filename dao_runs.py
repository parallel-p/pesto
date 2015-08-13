from model import Run


class DAORuns:
    columns = 'realtime, time, outcome, submit_ref, case_ref'

    def __init__(self, sqlite_connector):
        self.connector = sqlite_connector

    @staticmethod
    def load(row):
        run = Run('', '', '', row['realtime'], row['time'], row['outcome'])
        run.submit_ref, run.case_ref = row['submit_ref'], row['case_ref']
        return run

    def deep_load(self, row):
        run = self.load(row)
        cursor = self.connector.get_cursor()
        cursor.execute('SELECT case_id FROM Cases WHERE id = ?', [row['case_ref']])
        run.case_id = cursor.fetchone()['case_id']
        return run

    def define(self, submit_ref, case_ref):
        ref = self.lookup(submit_ref, case_ref)
        if ref is None:
            ref = self.create(submit_ref, case_ref)
        return ref

    def lookup(self, submit_ref, case_ref):
        cursor = self.connector.get_cursor()
        cursor.execute('SELECT id FROM Runs WHERE submit_ref = ? AND case_ref = ?',
                       [submit_ref, case_ref])
        response = cursor.fetchone()
        return response['id'] if response else None

    def create(self, submit_ref, case_ref):
        cursor = self.connector.get_cursor()
        cursor.execute('INSERT INTO Runs (id, submit_ref, case_ref) VALUES (NULL, ?, ?)',
                       [submit_ref, case_ref])
        return cursor.lastrowid

    def update(self, ref, update_def):
        cursor = self.connector.get_cursor()
        cursor.execute('SELECT {} FROM Runs WHERE id = ?'.format(self.columns), [ref])
        old = self.load(cursor.fetchone())
        new_def = {'submit_ref': old.submit_ref, 'case_ref': old.case_ref, 'realtime': old.real_time,
                   'time': old.time, 'outcome': old.outcome}
        for key, value in update_def.items():
            new_def[key] = value
        new_def['id'] = ref
        cursor.execute('UPDATE Runs SET submit_ref = :submit_ref, case_ref = :case_ref, realtime = :realtime, '
                       'time = :time, outcome = :outcome WHERE id = :id', new_def)
