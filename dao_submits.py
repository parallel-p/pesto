from model import Submit
from dao_runs import DAORuns


class DAOSubmits:
    columns = 'id, submit_id, lang_id, outcome, timestamp'

    def __init__(self, connector):
        self.connector = connector

    @staticmethod
    def load(row):
        if row is None:
            return None
        return Submit(row['submit_id'], ('', ''), '', row['lang_id'], [], row['outcome'], '', row['timestamp'])

    def deep_load(self, row):
        submit = DAOSubmits.load(row)
        cursor = self.connector.get_cursor()
        cursor.execute('SELECT {} FROM Runs WHERE submit_ref = ?'.format(DAORuns.columns), row['id'])
        runs_dao = DAORuns(self.connector)
        for run_row in cursor.fetchall():
            submit.runs.append(runs_dao.deep_load(run_row))
        submit.count_results()
        return submit
