from model import Submit
from dao_runs import DAORuns


class DAOSubmits:
    columns = 'id, submit_id, lang_id, problem_ref, user_ref, outcome, timestamp'

    def __init__(self, connector):
        self.connector = connector

    @staticmethod
    def load(row):
        submit = Submit(row['submit_id'], ('', ''), '', row['lang_id'], [], row['outcome'], '', row['timestamp'])
        submit.problem_ref, submit.user_ref = row['problem_ref'], row['user_ref']
        return submit

    def deep_load(self, row):
        submit = self.load(row)
        cursor = self.connector.get_cursor()
        cursor.execute('SELECT {} FROM Runs WHERE submit_ref = ?'.format(DAORuns.columns), (row['id'], ))
        runs_dao = DAORuns(self.connector)
        for run_row in cursor.fetchall():
            submit.runs.append(runs_dao.deep_load(run_row))
        submit.count_results()
        return submit

    def define(self, submit_id, problem_ref):
        ref = self.lookup(submit_id, problem_ref)
        if ref is None:
            ref = self.create(submit_id, problem_ref)
        return ref

    def lookup(self, submit_id, problem_ref):
        cursor = self.connector.get_cursor()
        cursor.execute('SELECT id FROM Submits WHERE submit_id = ? AND problem_ref = ?',
                       [submit_id, problem_ref])
        response = cursor.fetchone()
        return response['id'] if response else None

    def create(self, submit_id, problem_ref):
        cursor = self.connector.get_cursor()
        cursor.execute('INSERT INTO Submits (id, submit_id, problem_ref) VALUES (NULL, ?, ?)',
                       [submit_id, problem_ref])
        return cursor.lastrowid

    def update(self, ref, update_def):
        cursor = self.connector.get_cursor()
        cursor.execute('SELECT {} FROM Submits WHERE id = ?'.format(self.columns), ref)
        old = self.load(cursor.fetchone())
        new_def = {'submit_id': old.submit_id, 'lang_id': old.lang_id, 'problem_ref': old.problem_ref,
                   'user_ref': old.user_ref, 'outcome': old.outcome, 'timestamp': old.timestamp}
        for key, value in update_def.items():
            new_def[key] = value
        new_def['id'] = ref
        cursor.execute('UPDATE Submits SET submit_id = :submit_id, lang_id = :lang_id, problem_ref = :problem_ref, '
                       'user_ref = :user_ref, outcome = :outcome, timestamp = :timestamp WHERE id = :id', new_def)
