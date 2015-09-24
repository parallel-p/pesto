from model import User, Problem, Submit, Run
import model
import logging


class UsersDAO:
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


class ContestsDAO:
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
        cursor.execute('SELECT {} FROM Contests WHERE id = ?'.format(ContestsDAO.columns), [ref])
        old = self.load(cursor.fetchone())
        new_def = {'origin': old.origin, 'name': old.name, 'scoring': old.scoring, 'contest_id': old.contest_id}
        for key, value in update_def.items():
            new_def[key] = value
        new_def['id'] = ref
        cursor.execute('UPDATE Contests SET origin = :origin, name = :name, scoring = :scoring, '
                       'contest_id = :contest_id WHERE id = :id', new_def)


class CasesDAO:
    columns = "io_hash"

    def __init__(self, connector):
        self.connector = connector

    @staticmethod
    def load(row):
        result_hash = row['io_hash']
        return result_hash

    def deep_load(self, row):
        return self.load(row)

    def define(self, problem_ref, case_id):
        ref = self.lookup(problem_ref, case_id)
        if ref is None:
            ref = self.create(problem_ref, case_id)
        return ref

    def lookup(self, problem_ref, case_id):
        cursor = self.connector.get_cursor()
        cursor.execute('SELECT id FROM Cases WHERE problem_ref = ? AND case_id = ?', [problem_ref, case_id])
        response = cursor.fetchone()
        return response['id'] if response else None

    def create(self, problem_ref, case_id):
        cursor = self.connector.get_cursor()
        cursor.execute('INSERT INTO Cases (id, problem_ref, case_id) VALUES (NULL, ?, ?)', [problem_ref, case_id])
        return cursor.lastrowid

    def update(self, ref, update_def):
        cursor = self.connector.get_cursor()
        cursor.execute('SELECT {} FROM Cases WHERE id = ?'.format(self.columns), ref)
        old = self.load(cursor.fetchone())
        new_def = {'io_hash': old}
        for key, value in update_def.items():
            new_def[key] = value
        new_def['id'] = ref
        cursor.execute('UPDATE Cases SET io_hash = :io_hash WHERE id = :id', new_def)


class ProblemsDAO:
    columns = 'Problems.id, contest_ref, problem_id, Problems.name, polygon_id'

    def __init__(self, connector):
        self.connector = connector

    @staticmethod
    def load(row):
        result = Problem(('', row['problem_id']), row['polygon_id'], row['name'], [])
        result.contest_ref = row['contest_ref']
        result.db_id = row['id']  # kostil
        return result

    def deep_load(self, row, contest_id=None):
        result = self.load(row)
        cursor = self.connector.get_cursor()
        if contest_id is not None:
            result.problem_id = (contest_id, row['problem_id'])
        else:
            cursor.execute('SELECT contest_id FROM Contests WHERE id = ?', [row['contest_ref']])
            result.problem_id = (cursor.fetchone()['contest_id'], row['problem_id'])
        cursor.execute('SELECT {} FROM Cases WHERE problem_ref = ?'.format(CasesDAO.columns), [row['id']])
        cases_row = cursor.fetchone()
        while cases_row:
            hash = CasesDAO.load(cases_row)
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
        new_def = {'contest_ref': old.contest_ref, 'problem_id': old.problem_id[1], 'name': old.name, 'polygon_id': old.polygon_id}
        for key, value in update_def.items():
            new_def[key] = value
        new_def['id'] = ref
        cursor.execute('UPDATE Problems SET contest_ref = :contest_ref, name = :name, problem_id = :problem_id, polygon_id = :polygon_id, '
                       'WHERE id = :id', new_def)


class SubmitsDAO:
    columns = 'Submits.id, submit_id, lang_id, problem_ref, user_ref, outcome, timestamp'

    def __init__(self, connector):
        self.connector = connector

    @staticmethod
    def load(row):
        submit = Submit(row['submit_id'], ('', ''), '', row['lang_id'], [], row['outcome'], '', row['timestamp'])
        submit.problem_ref, submit.user_ref = row['problem_ref'], row['user_ref']
        return submit

    def deep_load(self, row, problem_id=None, scoring=None):
        submit = self.load(row)
        cursor = self.connector.get_cursor()
        cursor.execute('SELECT {} FROM Runs WHERE submit_ref = ?'.format(RunsDAO.columns), [row['id']])
        runs_dao = RunsDAO(self.connector)
        submit.runs = runs_dao.load_all(cursor.fetchall(), row['problem_ref'])
        submit.count_results()
        if problem_id is not None:
            submit.problem_id = problem_id
        else:
            logging.warning('SubmitsDAO: problem_id is not filled')
        if scoring is not None:
            submit.scoring = scoring
        else:
            logging.warning('SubmitsDAO: scoring is not filled')
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
        cursor.execute('SELECT {} FROM Submits WHERE id = ?'.format(self.columns), [ref])
        old = self.load(cursor.fetchone())
        new_def = {'submit_id': old.submit_id, 'lang_id': old.lang_id, 'problem_ref': old.problem_ref,
                   'user_ref': old.user_ref, 'outcome': old.outcome, 'timestamp': old.timestamp}
        for key, value in update_def.items():
            new_def[key] = value
        new_def['id'] = ref
        cursor.execute('UPDATE Submits SET submit_id = :submit_id, lang_id = :lang_id, problem_ref = :problem_ref, '
                       'user_ref = :user_ref, outcome = :outcome, timestamp = :timestamp WHERE id = :id', new_def)

class RunsDAO:
    columns = 'realtime, time, outcome, submit_ref, case_ref'
    case_cache = {}

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

    def load_all(self, rows, problem_ref):
        cursor = self.connector.get_cursor()
        runs = []
        if problem_ref in self.case_cache:
            cases = self.case_cache[problem_ref]
        else:
            cursor.execute('SELECT id,case_id FROM Cases WHERE problem_ref=?', (problem_ref,))
            cases = dict(cursor.fetchall())
            self.case_cache[problem_ref] = cases
        for row in rows:
            run = self.load(row)
            run.case_id = cases[row['case_ref']]
            runs.append(run)
        return runs


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
