from model import Problem
from dao_cases import DAOCases


class DAOProblems:
    def __init__(self, connector):
        self.connector = connector

    @staticmethod
    def load(row):
        result = Problem(row[2], row[3], [])
        return result

    def deep_load(self, row):
        result = DAOProblems.load(row)
        cursor = self.connector.get_cursor()
        cursor.execute('SELECT * FROM Cases WHERE problem_ref = ?', (row[0],))
        cases_row = cursor.fetchone()
        while cases_row:
            hash = DAOCases.load(cases_row)
            result.cases.append(hash)
            cases_row = cursor.fetchone()
        return result
