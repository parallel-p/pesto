from model import Problem
from dao_cases import DAOCases
import sys


class DAOProblems:
    columns = 'id, contest_ref, problem_id, name'

    def __init__(self, connector):
        self.connector = connector

    @staticmethod
    def load(row):
        result = Problem(('', row['problem_id']), '', row['name'], [])
        result.contest_ref = row['contest_ref']
        return result

    def deep_load(self, row):
        result = self.load(row)
        cursor = self.connector.get_cursor()
        cursor.execute('SELECT contest_id FROM Contests WHERE id = ?', [row['contest_ref']])
        result.problem_id = (cursor.fetchone()['contest_id'], row['problem_id'])
        cursor.execute('SELECT {} FROM Cases WHERE problem_ref = ?'.format(DAOCases.columns), [row['id']])
        cases_row = cursor.fetchone()
        while cases_row:
            hash = DAOCases.load(cases_row)
            result.cases.append(hash)
            cases_row = cursor.fetchone()
        return result

    def define(self, contest_ref, problem_id):
        ref = self.lookup(contest_ref, problem_id)
        if ref is None:
            ref = self.create(contest_ref, problem_id)
        return ref

    def lookup(self, contest_ref, problem_id):
        cursor = self.connector.get_cursor()
        cursor.execute('SELECT id FROM Problems WHERE contest_ref = ? AND problem_id = ?',
                       [contest_ref, problem_id])
        response = cursor.fetchone()
        return response['id'] if response else None

    def create(self, contest_ref, problem_id):
        cursor = self.connector.get_cursor()
        cursor.execute('INSERT INTO Problems (id, contest_ref, problem_id) VALUES (NULL, ?, ?)',
                       [contest_ref, problem_id])
        return cursor.lastrowid

    def update(self, ref, update_def):
        cursor = self.connector.get_cursor()
        cursor.execute('SELECT {} FROM Problems WHERE id = ?'.format(self.columns), [ref])
        old = self.load(cursor.fetchone())
        new_def = {'contest_ref': old.contest_ref, 'problem_id': old.problem_id[1], 'name': old.name}
        for key, value in update_def.items():
            new_def[key] = value
        new_def['id'] = ref
        cursor.execute('UPDATE Problems SET contest_ref = :contest_ref, name = :name, problem_id = :problem_id '
                       'WHERE id = :id', new_def)
