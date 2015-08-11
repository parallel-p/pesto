from model import Run


class DAORuns:
    def __init__(self, sqlite_connector):
        self.connector = sqlite_connector

    @staticmethod
    def load(row):
        real_time = row['real_time']
        time = row['time']
        outcome = row['outcome']
        run = Run('', '', '', real_time, time, outcome)
        return run

    def deep_load(self, row):
        real_time, time, outcome, case_ref = row['real_time'], row['time'], row['outcome'], row['case_ref']
        cursor = self.connector.get_cursor()
        cursor.execute('SELECT case_id '
                       'FROM cases '
                       'WHERE cases.id=?', case_ref)

        case_id = cursor.fetchone()
        run = Run('', '', case_id, real_time, time, outcome)
        return run