from model import Problem
from dao_cases import DAOCases


class DAOProblems:
    columns = 'id, contest_ref, problem_id, name'

    def __init__(self, connector):
        self.connector = connector

    @staticmethod
    def load(row):
        result = Problem(('', row['problem_id']), row['name'], [])
        return result

    def deep_load(self, row):
        result = DAOProblems.load(row)
        cursor = self.connector.get_cursor()
        cursor.execute('SELECT contest_id FROM Contests WHERE id = ?', (row['contest_ref'],))
        result.problem_id = (row['problem_id'], cursor.fetchone()[0])
        cursor.execute('SELECT {} FROM Cases WHERE problem_ref = ?'.format(DAOCases.columns), (row['id'],))
        cases_row = cursor.fetchone()
        while cases_row:
            hash = DAOCases.load(cases_row)
            result.cases.append(hash)
            cases_row = cursor.fetchone()
        return result
