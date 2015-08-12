from model import Run


class DAORuns:
    columns = 'realtime, time, outcome, case_ref'

    def __init__(self, sqlite_connector):
        self.connector = sqlite_connector

    @staticmethod
    def load(row):
        real_time = row['realtime']
        time = row['time']
        outcome = row['outcome']
        run = Run('', '', '', real_time, time, outcome)
        return run

    def deep_load(self, row):
        real_time, time, outcome, case_ref = row['realtime'], row['time'], row['outcome'], row['case_ref']
        cursor = self.connector.get_cursor()
        cursor.execute('SELECT case_id '
                       'FROM cases '
                       'WHERE cases.id=?', (case_ref, ))

        case_id = tuple(cursor.fetchone())[0]
        run = Run('', '', case_id, real_time, time, outcome)
        return run
